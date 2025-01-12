"""Node setup wizard logic."""

import logging
import sys
import typing
import dataclasses

import click

from baymesh.cli import devices, echo
from meshtastic.protobuf import config_pb2

if typing.TYPE_CHECKING:
    from typing import Callable
    import meshtastic.serial_interface

    LoraPresetValueType = config_pb2.Config.LoRaConfig.ModemPreset.ValueType
    DeviceRoleValueType = config_pb2.Config.DeviceConfig.Role.ValueType


class SetupWizard(object):
    """Contains a guided flow for collecting settings from users."""

    def __init__(self):
        self._settings: "ConfigsToApply" = ConfigsToApply()
        self._current_prompt = None
        self._is_active = False

    def run(self) -> "ConfigsToApply":
        """Begin the interactive guided flow and return the configs when done."""
        self._settings = ConfigsToApply()
        self._current_prompt = self._prompt_lora_preset
        self._is_active = True
        while self._is_active:
            self._current_prompt()
        return self._settings

    def _set_prompt_func(self, prompt: "Callable"):
        """Set the prompt function to call on the next self.run() iteration."""
        self._current_prompt = prompt

    def _finish(self):
        """Complete the process of gathering settings from the user."""
        # Setting this to False causes the while loop in self.run() to fall through.
        self._is_active = False

    def _prompt_lora_preset(self):
        use_medium_slow = echo.confirm(
            message="Use MEDIUM_SLOW LoRa preset?",
            additional_info="Start with MEDIUM_SLOW. Return and answer No if you can't find other nodes.",
            default=True,
        )
        if use_medium_slow:
            self._settings.lora_preset = (
                config_pb2.Config.LoRaConfig.ModemPreset.MEDIUM_SLOW
            )
        else:
            self._settings.lora_preset = (
                config_pb2.Config.LoRaConfig.ModemPreset.LONG_FAST
            )
        self._set_prompt_func(self._prompt_long_name)

    def _prompt_long_name(self):
        long_name = echo.prompt(
            message="What would you like this node's long name to be?",
            additional_info="This is typically your name, Discord handle, or Ham callsign",
        )
        self._settings.device_long_name = long_name
        self._set_prompt_func(self._prompt_short_name)

    def _prompt_short_name(self):
        short_name = echo.prompt(
            message="What would you like this node's short name to be?",
            additional_info="This can be up to four characters long and can even be an emoji",
        )
        if len(short_name) > 4:
            echo.error("Short name must be no longer than four characters.")
            return
        self._settings.device_short_name = short_name
        self._set_prompt_func(self._prompt_device_role)

    def _prompt_device_role(self):
        is_relay = echo.confirm(
            message="Should this node relay messages from other nodes to other nodes in the mesh?",
            additional_info=[
                "If this is your primary node or a home base station, answer Y(yes).",
                "If this node will be in close proximity to other nodes who are already relaying messages, answer N(no)",
            ],
            default=True,
        )
        if is_relay:
            device_role = config_pb2.Config.DeviceConfig.Role.CLIENT
        else:
            device_role = config_pb2.Config.DeviceConfig.Role.CLIENT_MUTE
        self._settings.device_role = device_role
        self._set_prompt_func(self._prompt_confirm_settings)

    def _prompt_confirm_settings(self):
        click.secho("\nSettings preview: not yet applied to device", bold=True)
        click.echo(self._settings)
        is_satisfied = echo.confirm("Apply these configs to your device?", default=True)
        if is_satisfied:
            self._finish()
        else:
            click.echo("Canceling setup and exiting.")
            sys.exit(0)


@dataclasses.dataclass
class ConfigsToApply(object):
    """Simplified local configs container for the setup wizard."""

    device_long_name: str = ""
    device_short_name: str = ""

    lora_preset: "LoraPresetValueType" = (
        config_pb2.Config.LoRaConfig.ModemPreset.MEDIUM_SLOW
    )
    device_role: "DeviceRoleValueType" = config_pb2.Config.DeviceConfig.Role.CLIENT

    telemetry_device_update_interval: int = 3600
    telemetry_environment_update_interval: int = 3600
    telemetry_power_update_interval: int = 3600

    @property
    def lora_preset_name(self) -> str:
        """String form of the selected LoRa preset."""
        return config_pb2.Config.LoRaConfig.ModemPreset.Name(self.lora_preset)

    @property
    def device_role_name(self) -> str:
        """String form of the selected device role."""
        return config_pb2.Config.DeviceConfig.Role.Name(self.device_role)

    def __str__(self):
        return (
            f"Long name: {self.device_long_name}\n"
            f"Short name: {self.device_short_name}\n"
            f"LoRa preset: {self.lora_preset_name}\n"
            f"Role: {self.device_role_name}\n"
        )


def apply_configs(
    configs: ConfigsToApply, interface: "meshtastic.serial_interface.SerialInterface"
):
    """Applies the configs based on the users responses to the setup wizard."""
    our_node: meshtastic.Node = interface.getNode("^local")
    original_level = echo.get_logging_level()
    echo.set_logging_level(logging.ERROR)

    click.secho("⚙️  Applying long and short name...")
    # This doesn't seem to reboot the node...
    our_node.setOwner(
        long_name=configs.device_long_name, short_name=configs.device_short_name
    )

    devices.wait_for_settings_to_apply()

    click.secho("⚙️  Applying LoRa configs...")
    our_node.localConfig.lora.use_preset = True
    our_node.localConfig.lora.region = config_pb2.Config.LoRaConfig.RegionCode.US
    our_node.localConfig.lora.modem_preset = configs.lora_preset
    our_node.localConfig.lora.config_ok_to_mqtt = True
    our_node.writeConfig("lora")

    devices.wait_for_settings_to_apply()

    click.secho("⚙️  Applying role configs...")
    our_node.localConfig.device.role = configs.device_role
    our_node.writeConfig("device")
    echo.set_logging_level(original_level)
