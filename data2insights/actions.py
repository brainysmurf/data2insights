from click.testing import CliRunner
from .cli import main


def homeroom():

    runner = CliRunner()
    result = runner.invoke(
        main, ["target", "--type", "gcloud", "source", "--type", "gcloud", "action"]
    )
    print(result.output)
