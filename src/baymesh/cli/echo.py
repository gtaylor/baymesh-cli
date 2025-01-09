"""Logic for echoing with formatting in a consistent manner."""

import enum
import typing
import logging

import click

from baymesh import node_validation

if typing.TYPE_CHECKING:
    from typing import Callable, Any


# TODO: Color constants


def error(message):
    """Indicate that an error has occurred."""
    click.secho(f"🚨 {message}", fg="red", bold=True)


def success(message):
    """Indicate that a success has occurred."""
    click.secho(f"✅ {message}", fg="green", bold=True)


def warning(message):
    """Non-blocking warning."""
    click.secho(f"⚠️ {message}", fg="yellow")


def info(message):
    """Share context or progress."""
    click.secho(f"️ℹ️ {message}", fg="cyan")


def working(message):
    """Share progress."""
    click.secho(f"⚙️ {message}")


def confirm(message: str, additional_info: str | list[str] = "", **kwargs) -> bool:
    """Prompts the user for a confirmation."""
    msg_contents = click.style(f"🤔 {message}", fg="cyan")
    # TODO: Dedupe
    if additional_info and isinstance(additional_info, str):
        additional_info = [additional_info]
    if additional_info:
        for additional_info_nugget in additional_info:
            msg_contents += f"\n     {additional_info_nugget}"
    return click.confirm(msg_contents, **kwargs)


def prompt(message: str, additional_info: str | list[str] = "", **kwargs) -> "Any":
    """Prompts the user."""
    msg_contents = click.style(f"🤔 {message}", fg="cyan")
    if additional_info and isinstance(additional_info, str):
        additional_info = [additional_info]
    if additional_info:
        for additional_info_nugget in additional_info:
            msg_contents += f"\n     {additional_info_nugget}"
    return click.prompt(msg_contents, **kwargs)


def set_logging_level(level: int, logger=None):
    """Sets the specified logger to the given level."""
    logger = logging.getLogger(logger)
    logger.setLevel(level)


def _recommendation_severity_to_echo(severity: "enum.Enum") -> "Callable":
    """Maps a recommendation severity to the corresponding echo func."""
    match severity:
        case node_validation.RecommendationSeverity.ERROR:
            return error
        case node_validation.RecommendationSeverity.WARNING:
            return warning
        case _:
            return info
