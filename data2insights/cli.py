import click
from .services import Service
from .sheets import GSheet
from dotenv import load_dotenv

load_dotenv()


@click.command()
@click.option("--id", "id_", required=True, envvar="GSHEET_ID", show_envvar=True)
def main(id_):

    service = Service()
    spreadsheet = GSheet(service, id_)

    df = spreadsheet.document.read_tab("Sheet1")
    print(df)
