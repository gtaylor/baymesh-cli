"""Logic for echoing with formatting in a consistent manner."""

import enum
import typing
import logging

import click

from baymesh import node_validation

if typing.TYPE_CHECKING:
    from typing import Callable, Any


ERROR_COLOR = "red"
SUCCESS_COLOR = "green"
WARNING_COLOR = "yellow"
PROMPT_COLOR = "cyan"


def error(message):
    """Indicate that an error has occurred."""
    click.secho(f"🚨 {message}", fg=ERROR_COLOR, bold=True)


def success(message):
    """Indicate that a success has occurred."""
    click.secho(f"✅ {message}", fg=SUCCESS_COLOR, bold=True)


def warning(message):
    """Non-blocking warning."""
    click.secho(f"⚠️  {message}", fg=WARNING_COLOR)


def info(message):
    """Share context or progress."""
    click.secho(f"️ℹ️  {message}")


def working(message):
    """Share progress."""
    click.secho(f"⚙️  {message}")


def _buffer_additional_info(additional_info: str | list[str]) -> str:
    """Convenience function for formatting additional info beneath a prompt."""
    if not additional_info:
        return ""
    if isinstance(additional_info, str):
        additional_info = [additional_info]
    buf = ""
    for additional_info_nugget in additional_info:
        buf += f"\n     {additional_info_nugget}"
    return buf


def confirm(message: str, additional_info: str | list[str] = "", **kwargs) -> bool:
    """Prompts the user for a confirmation."""
    msg_contents = click.style(f"🤔 {message}", fg=PROMPT_COLOR)
    msg_contents += _buffer_additional_info(additional_info)
    return click.confirm(msg_contents, **kwargs)


def prompt(message: str, additional_info: str | list[str] = "", **kwargs) -> "Any":
    """Prompts the user."""
    msg_contents = click.style(f"🤔 {message}", fg=PROMPT_COLOR)
    msg_contents += _buffer_additional_info(additional_info)
    return click.prompt(msg_contents, **kwargs)


def get_logging_level(logger=None) -> int:
    """Gets the current level for the given logger."""
    logger = logging.getLogger(logger)
    return logger.getEffectiveLevel()


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
