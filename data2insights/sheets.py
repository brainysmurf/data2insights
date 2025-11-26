from google.colab import auth
from google.auth import default
import gspread
from dataclasses import dataclass, field


@dataclass
class Doc:
    spreadsheet: gspread.Spreadsheet


@dataclass
class GSheet:
    """
    Initialize a spreadsheet for convenience
    """

    spreadsheet_id: str  # req
    open_: bool = True  # open by default
    document: Doc = field(init=False)  # let me init

    def __post_init__(self, open_: bool = True):
        """
        Authenticate with google and authorize utiltites
        spreadsheet_id: The ID from the URL of the spreadsheet

        -> Will have .document
        """
        auth.authenticate_user()
        self.creds, _ = default()
        gc = gspread.authorize(self.creds)
        if open_:
            self.open_by_key()

    def open_by_key(self) -> Doc:
        self.document = Doc(gc.open_by_key(self.spreadsheet_id))
        return self.document
