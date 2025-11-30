import click
from dataclasses import dataclass
from .services import Service
from typing import Any


@dataclass
class ServiceCtx:
    service: Service


@dataclass
class SourceCtx:
    document: Any


@dataclass
class TargetCtx:
    document: Any


pass_service_ctx = click.make_pass_decorator(ServiceCtx)
pass_source_ctx = click.make_pass_decorator(SourceCtx)
pass_target_ctx = click.make_pass_decorator(TargetCtx)
