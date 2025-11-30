from click.testing import CliRunner
from .cli import main


def homeroom(id_):

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
            "action",
        ],
    )
    print(result.output)
