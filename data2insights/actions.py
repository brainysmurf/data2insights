from click.testing import CliRunner
from .cli import main


def prepare_housepoint_tallying(id_):

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "target",
            "--type",
            "gcloud",
            "--id",
            id_,
            "source",
            "--type",
            "gcloud",
            "--id",
            id_,
            "scenario:housepoints:setup",
        ],
    )

    runner.invoke(
        main,
        [
            "target",
            "--type",
            "duckdb",
            "source",
            "--type",
            "gcloud",
            "--id",
            id_,
            "scenario:housepoints:calculate",
        ],
    )

    print(result.output)
