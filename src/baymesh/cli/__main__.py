"""Primary CLI entrypoint."""

import typing
import logging

import click

from baymesh import node_validation, baymesh_versions
from baymesh.cli import devices, node_setup, echo

if typing.TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


@click.group(no_args_is_help=True)
@click.pass_context
def cli(ctx: click.Context):
    """Node setup, validation, and management CLI for the Meshtastic Bay Area Group."""
    ctx.ensure_object(dict)
    try:
        is_up_to_date, latest_version = baymesh_versions.is_up_to_date()
    except RuntimeError as exc:
        logger.warning(f"Unable to determine latest version of baymesh: {exc}")
        return
    if not is_up_to_date:
        echo.warning(
            f"A new version ({latest_version}) of the baymesh CLI is available. "
            f"Please upgrade in order to ensure continued interop with the mesh."
        )


@cli.command()
def validate():
    """Validates that a connected node conforms to Baymesh standards."""
    port = devices.select_device_flow()
    interface = devices.ensure_meshtastic_interface(device_path=port.device, port=port)
    report = node_validation.validate_node(interface=interface)
    devices.announce_connected_device(interface)
    echo.working("Validating node configs...\n")
    node_validation.render_validation_report(report)


@cli.command()
def setup():
    """Sets up a node using the standard Baymesh configs."""
    port = devices.select_device_flow()
    interface = devices.ensure_meshtastic_interface(device_path=port.device, port=port)
    devices.announce_connected_device(interface)
    echo.confirm(
        "If you have already configured your node, the setup wizard will "
        "overwrite some of your settings. Continue?"
    )
    echo.working("Starting setup wizard...\n")
    setup_wizard = node_setup.SetupWizard()
    configs = setup_wizard.run()
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
