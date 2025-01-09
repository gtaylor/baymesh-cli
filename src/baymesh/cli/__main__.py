"""Primary CLI entrypoint."""

import typing

import click

from baymesh import node_validation
from baymesh.cli import devices, node_setup, echo

if typing.TYPE_CHECKING:
    pass


@click.group(no_args_is_help=True)
@click.pass_context
def cli(ctx: click.Context):
    """Node setup, validation, and management CLI for the Meshtastic Bay Area Group."""
    ctx.ensure_object(dict)


def _render_validation_report(report: "node_validation.Report"):
    """Renders the validation report for consumption by the user."""
    success_msg = "Your node is compliant with all Meshtastic Bay Area Group standards!"
    if not report.list_recommendations():
        echo.success(success_msg)
        return

    for recommendation in report.recommendations:
        echo_func = echo._recommendation_severity_to_echo(recommendation.severity)
        echo_func(f"{ recommendation.severity.name }: { recommendation.message }")

    if report.validation_successful():
        echo.success(f"{ success_msg } Please consider the above warning(s).")
    else:
        echo.error(
            "Your node is not complaint with Meshtastic Bay Area Group standards "
            "due to the above error(s)."
        )


@cli.command()
def validate():
    """Validates that a connected node conforms to Baymesh standards."""
    port = devices.select_device_flow()
    interface = devices.ensure_meshtastic_interface(device_path=port.device, port=port)
    report = node_validation.validate_node(interface=interface)
    echo.info(
        f"Found Meshtastic node: { report.device_long_name } ({report.device_short_name})"
    )
    echo.working("Validating node configs...\n")
    _render_validation_report(report)


@cli.command()
def setup():
    """Sets up a node using the standard Baymesh configs."""
    port = devices.select_device_flow()
    interface = devices.ensure_meshtastic_interface(device_path=port.device, port=port)
    echo.confirm(
        "If you have already configured your node, the setup wizard may "
        "overwrite some of your settings. Continue?"
    )
    echo.working("Starting setup wizard...\n")
    configs = node_setup.run_setup_wizard()
    node_setup.apply_configs(configs, interface)
    echo.success("Device configured. Happy meshing!")


@cli.command()
def detect_devices():
    """Attempts to automatically detect supported devices.

    Only detects USB devices at the moment!
    """
    ports = devices.detect_supported_devices_via_serial()
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
