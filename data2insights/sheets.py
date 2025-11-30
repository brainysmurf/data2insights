from dataclasses import dataclass, field
import gspread
from .services import Service
import google
import pandas as pd
import logging
import pathlib
import json
from io import StringIO
from gspread_dataframe import set_with_dataframe

logger = logging.getLogger(__name__)


@dataclass
class AbstractDoc:

    @classmethod
    def convert_data_to_df(cls, data):
        raise NotImplemented

    def read_tab(self, title):
        raise NotImplemented


@dataclass
class Dir(AbstractDoc):
    """A folder with files"""

    path: pathlib.Path

    @classmethod
    def convert_data_to_df(cls, data):
        return pd.read_json(StringIO(data))

    def read_tab(self, title):
        source = self.path / title
        with open(source.with_suffix(".json")) as f_:
            data = f_.read()
            return Dir.convert_data_to_df(data)

    def save_records(self, title, records):
        source = self.path / title
        df = pd.DataFrame.from_records(records)
        with open(source.with_suffix(".json"), "w") as f_:
            f_.write(df.to_json())


@dataclass
class Worksheet(AbstractDoc):
    spreadsheet: gspread.Spreadsheet

    @classmethod
    def convert_data_to_df(cls, data):
        return pd.DataFrame(data[1:], columns=data[0])  # first row as header

    def read_tab(self, title):
        tab = self.spreadsheet.worksheet(title)
        # 4. Get all values as a list of lists
        data = tab.get_all_values()
        logger.info(f"Pulled {len(data)} rows of data")

        # 5. Convert to a DataFrame
        return Worksheet.convert_data_to_df(data)

    def write_tab(self, title, df):
        rows, cols = df.shape
        if title in [tab.title for tab in self.spreadsheet.worksheets()]:
            tab = self.spreadsheet.worksheet(title)
        else:
            tab = self.spreadsheet.add_worksheet(
                title=title, rows=max(rows + 1, 10), cols=max(cols, 5)
            )

        set_with_dataframe(tab, df)
        logger.info(f"Wrote {rows + 1} rows and {cols} cols")


@dataclass
class GSheet:
    """
    Initialize a spreadsheet for convenience
    """

    service: Service
    spreadsheet_id: str  # req
    open_: bool = True  # open by default
    client: google.oauth2.service_account.Credentials = field(init=False)
    document: Worksheet = field(init=False)  # let me init

    def __post_init__(self):
        """
        Create client to interact with google spreadsheets
        """
        self.client = gspread.Client(auth=self.service.creds)
        if self.open_:
            self.open()
        else:
            self.document = None

    def open(self) -> Worksheet:
        spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        self.document = Worksheet(spreadsheet)
        return self.document

    def __getattr__(self, name):
        if hasattr(self.document, name):
            return getattr(self.document, name)
        else:
            if self.document is None:
                raise Exception(f"Worksheet is None, did you open it?")
            raise AttributeError(f"GSheet or Worksheet does not have {name}")

    @classmethod
    def scopes(cls):
        """Scopes needed on the service account"""
        return ["https://www.googleapis.com/auth/spreadsheets"]


@dataclass
class Directory:
    path: pathlib.Path
    document: Dir = field(init=False)

    def open(self) -> Dir:
        self.document = Dir(self.path)
        return self.document
