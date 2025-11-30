import click
from .services import Service
from .sheets import GSheet
from .sheets import Directory
from .contexts import ServiceCtx, SourceCtx, TargetCtx
from .contexts import pass_service_ctx, pass_source_ctx, pass_target_ctx
import pathlib
from .utils import make_keyword_validator, TYPE_KEYWORDS, SOURCE_KEYWORDS
from .utils import find_value


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = ServiceCtx(Service())


@main.group()
@click.option("--type", "type_", type=click.Choice(TYPE_KEYWORDS.keys()))
@click.option(
    "--keyword",
    "keywords",
    multiple=True,
    type=(str, str),
    callback=make_keyword_validator(TYPE_KEYWORDS),
)
@click.option("--id", "id_", envvar="GSHEET_ID", show_envvar=True)
@pass_service_ctx
@click.pass_context
def target(ctx, service, type_, keywords, **kwargs):
    """
    Define the target source
    """
    if type_ == "gcloud":
        doc = GSheet(service.service, find_value("id_", keywords, kwargs))
    elif type_ == "screen":
        print("Can't handle screen yet!")
        doc = None
    else:
        raise click.BadParameter(type_)

    ctx.obj = TargetCtx(doc)


@target.group()
@click.option("--type", "type_", type=click.Choice(TYPE_KEYWORDS.keys()))
@click.option(
    "--keyword",
    "keywords",
    multiple=True,
    type=(str, str),
    callback=make_keyword_validator(SOURCE_KEYWORDS),
)
@click.option("--id", "id_", envvar="GSHEET_ID", show_envvar=True)
@pass_service_ctx
@click.pass_context
def source(ctx, service, type_, keywords, **kwargs):
    """
    Define the data source
    """
    if type_ == "gcloud":
        doc = GSheet(service.service, find_value("id_", keywords, kwargs))
    else:
        raise click.BadParameter(type_)

    ctx.obj = SourceCtx(doc)


@source.command()
@pass_target_ctx
@pass_source_ctx
def action(source, target):
    df = source.document.read_tab("Sheet1")
    target.document.write_tab("Here", df)
    breakpoint()


# @main.command()
# @click.option("--id", "id_", envvar="GSHEET_ID", show_envvar=True)
# @click.option(
#     "--json_path",
#     "json_path",
#     type=click.Path(),
#     envvar="PATH_TO_JSON",
#     show_envvar=True,
# )
# @pass_service_ctx
# @click.pass_context
# def source(ctx, service_ctx: ServiceCtx, id_: str, json_path: str):

#     if id_ is not None:
#         source = GSheet(service_ctx.service, id_, open_=False)

#     elif json_path is not None:
#         source = ...

#     ctx.obj = SourceCtx(source)


# @main.group()
# @click.option("--path", type=click.Path(), required=True)
# @pass_service_ctx
# @click.pass_context
# def local_files(ctx, service_ctx: ServiceCtx, path: pathlib.Path):
#     path = pathlib.Path(path)
#     source = Directory(path)
#     document = source.open()
#     ctx.obj = SourceCtx(document)


# @local_files.command()
# @pass_source_ctx
# def housepoint_seeds(source_ctx):
#     doc = source_ctx.document

#     records = []
#     for id_ in range(1000, 1000 * 10):
#         record = {"id": id_, "name": "Name", "house": "House"}
#         records.append(record)

#     doc.save_records("students", records)


# @local_files.command()
# @pass_source_ctx
# def housepoints(source_ctx):
#     doc = source_ctx.document
#     print(doc)
