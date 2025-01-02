"""Primary CLI entrypoint."""

import typing
import functools

import click

from baymesh import connection_management, node_validation

if typing.TYPE_CHECKING:
    import enum
    from serial.tools.list_ports_common import ListPortInfo


@click.group(no_args_is_help=True)
@click.pass_context
def cli(ctx: click.Context):
    """Node setup, validation, and management CLI for the Meshtastic Bay Area Group."""
    ctx.ensure_object(dict)


def add_node_config_option(f):
    """Reusable decorator for adding a standard node config option.

    Appends the config_path arg to the end of the command function's params.
    """

    @click.option(
        "-c",
        "--config-path",
        type=click.Path(exists=True, dir_okay=False),
        help="Path to baymesh.yaml config file",
        default="baymesh.yaml",
    )
    @functools.wraps(f)
    def new_func(*args, config_path, **kwargs):
        return f(*args, config_path, **kwargs)

    return new_func


def _select_device_flow() -> "ListPortInfo":
    """If multiple supported devices are connected, prompt the user to select one."""
    ports = connection_management.detect_supported_devices_via_serial()
    if not ports:
        raise click.UsageError("Could not find a supported device connected via USB.")
    if len(ports) == 1:
        # Only one device, no need to prompt!
        return ports[0]

    while True:
        click.echo("Found multiple supported devices:")
        for i, port in enumerate(ports):
            click.echo(f"{i}) {port.device} - {port.description} - {port.hwid}")
        num_selected = int(
            click.prompt(
                "Which device number would you like to validate?",
                type=click.Choice(list(str(c) for c in range(len(ports)))),
            )
        )
        return ports[num_selected]


def _recommendation_severity_to_color(severity: "enum.Enum") -> str:
    """Maps a recommendation severity to a color for output."""
    match severity:
        case node_validation.RecommendationSeverity.ERROR:
            return "red"
        case node_validation.RecommendationSeverity.WARNING:
            return "yellow"
        case _:
            return "cyan"


def _recommendation_severity_to_emoji(severity: "enum.Enum") -> str:
    """Maps a recommendation severity to an emoji prefix for output."""
    match severity:
        case node_validation.RecommendationSeverity.ERROR:
            return "🚨"
        case node_validation.RecommendationSeverity.WARNING:
            return "⚠️"
        case _:
            return "ℹ️"


def _render_validation_report(report: "node_validation.Report"):
    """Renders the validation report for consumption by the user."""
    success_msg = (
        "✅ Your node is compliant with all Meshtastic Bay Area Group standards!"
    )
    if not report.list_recommendations():
        click.secho(message=success_msg, fg="green", bold=True)
        return

    for recommendation in report.recommendations:
        emoji = _recommendation_severity_to_emoji(recommendation.severity)
        fg_color = _recommendation_severity_to_color(recommendation.severity)
        click.secho(
            f"{emoji}  { recommendation.severity.name }: { recommendation.message }",
            fg=fg_color,
        )

    if report.validation_successful():
        click.secho(
            f"{ success_msg } Please consider the above warning(s).",
            fg="green",
            bold=True,
        )
    else:
        click.secho(
            "Your node is not complaint with Meshtastic Bay Area Group standards "
            "due to the above error(s).",
            fg="red",
            bold=True,
        )


@cli.command()
def validate():
    """Validates that a connected node conforms to Baymesh standards."""
    port = _select_device_flow()
    click.echo(f"⚙️  Opening connection to {port.description} via {port.device}...")
    report = node_validation.validate_node(device_path=port.device)
    click.echo(
        f"⚙️  Found Meshtastic node: { report.device_long_name } ({report.device_short_name})"
    )
    _render_validation_report(report)


@cli.command()
def detect_devices():
    """Attempts to automatically detect supported devices.

    Only detects USB devices at the moment!
    """
    ports = connection_management.detect_supported_devices_via_serial()
    if not ports:
        click.echo("No supported devices found.")
        return
    click.echo("Found potentially supported devices:")
    for port in ports:
        click.echo(f"* {port.device}")
        click.echo(f"    Description: {port.description}")
        click.echo(f"           HWID: {port.hwid}")


if __name__ == "__main__":
    cli(obj={})
