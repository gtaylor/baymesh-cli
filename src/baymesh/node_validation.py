"""Logic for validating that nodes comply with Bay Mesh standards.

See:
* https://bayme.sh/docs/getting-started/recommended-settings/
* https://bayme.sh/docs/getting-started/mqtt/
"""

import enum
import dataclasses
import typing
from typing import Any

from baymesh.cli import echo
from meshtastic.protobuf import config_pb2, channel_pb2

from baymesh import firmware_versions

if typing.TYPE_CHECKING:
    import meshtastic.serial_interface


class RecommendationSeverity(enum.Enum):
    """Determines how much of an issue a report finding is."""

    # "Take it or leave it" advice.
    TIP = 1
    # "You should probably fix this, but it's not the end of the world if not".
    WARNING = 2
    # "You should *definitely* fix this unless you've got extenuating circumstances".
    ERROR = 3


@dataclasses.dataclass
class Recommendation(object):
    """Contains a single finding."""

    # The guidance that is provided to the user.
    message: str
    # A measure of how severe the issue is.
    severity: enum.Enum


@dataclasses.dataclass
class Report(object):
    """Contains a summarized report of findings for the user to consume."""

    # The device's long name, for display.
    device_long_name: str
    # The device's short name, also for display.
    device_short_name: str
    # A list of findings.
    recommendations: list[Recommendation] = dataclasses.field(default_factory=list)

    def add_recommendations(self, recommendations: list[Recommendation | None]):
        """Adds a recommendation to the report."""
        for recommendation in recommendations:
            if not recommendation:
                continue
            self.recommendations += (recommendation,)

    def list_recommendations(self, only_severity=None) -> list[Recommendation]:
        """Lists (and optionally filters) the report's recommendations."""
        if not only_severity:
            return self.recommendations
        matches = []
        for recommendation in self.recommendations:
            if recommendation.severity == only_severity:
                matches.append(recommendation)
        return matches

    def validation_successful(self) -> bool:
        """Returns True if the node complies with all essential standards."""
        errors = self.list_recommendations(only_severity=RecommendationSeverity.ERROR)
        return len(errors) == 0


def validate_node(interface: "meshtastic.serial_interface.SerialInterface") -> Report:
    """Given a serial path, validate the attached device for compliance."""
    node_info: dict[str, Any] | None = interface.getMyNodeInfo()
    if not node_info:
        raise RuntimeError("Failed to get node info. Please try again.")
    our_node: meshtastic.Node = interface.getNode("^local")

    report = Report(
        device_long_name=node_info["user"]["longName"],
        device_short_name=node_info["user"]["shortName"],
    )
    # Run through all of the validation functions for the things that we care about.
    # Recommendations will be shown to the user in the order that the checking functions
    # appear below.
    report.add_recommendations(
        [
            _check_user_long_name(long_name=node_info["user"]["longName"]),
            _check_lora_region(region=our_node.localConfig.lora.region),
            _check_lora_preset(
                use_preset=our_node.localConfig.lora.use_preset,
                modem_preset=our_node.localConfig.lora.modem_preset,
            ),
            _check_lora_hop_limit(hop_limit=our_node.localConfig.lora.hop_limit),
            _check_device_role(role=our_node.localConfig.device.role),
            _check_module_telemetry_update_interval(
                telemetry_type="device",
                update_interval=our_node.moduleConfig.telemetry.device_update_interval,
            ),
            _check_module_telemetry_update_interval(
                telemetry_type="environment",
                update_interval=our_node.moduleConfig.telemetry.environment_update_interval,
            ),
            _check_module_telemetry_update_interval(
                telemetry_type="power",
                update_interval=our_node.moduleConfig.telemetry.power_update_interval,
            ),
            _check_node_firmware_version(
                node_firmware_version=firmware_versions.get_node_firmware_version(
                    our_node
                ),
                latest_firmware_version=firmware_versions.get_latest_firmware_version(),
            ),
            _check_channels_mqtt_settings(
                channels=our_node.channels,
            ),
        ]
    )

    interface.close()
    return report


def _check_user_long_name(long_name: str) -> Recommendation | None:
    """Suggest that the user set a long name if it looks like they've got the default."""
    split_name = long_name.split()
    if len(split_name) == 2 and split_name[0] == "Meshtastic" and len(split_name[1]) == 4:
        return Recommendation(
            message=f"Your node's long name '{long_name}' is close to the default. "
            f"Consider setting a more descriptive long name.",
            severity=RecommendationSeverity.WARNING,
        )


def _check_lora_region(
    region: config_pb2.Config.LoRaConfig.RegionCode.ValueType,
) -> Recommendation | None:
    """Ensure that the user has selected the correct region."""
    if not region == config_pb2.Config.LoRaConfig.RegionCode.US:
        region_name = config_pb2.Config.LoRaConfig.RegionCode.Name(region)
        return Recommendation(
            message=f"Region is set to {region_name} instead of US.",
            severity=RecommendationSeverity.ERROR,
        )


def _check_lora_preset(use_preset: bool, modem_preset: int) -> Recommendation | None:
    if (
        not use_preset
        or modem_preset != config_pb2.Config.LoRaConfig.ModemPreset.MEDIUM_SLOW
    ):
        """Ensure that the user is using the MEDIUM_SLOW preset."""
        return Recommendation(
            message="Lora preset is not set to MEDIUM_SLOW.",
            severity=RecommendationSeverity.ERROR,
        )


def _check_lora_hop_limit(hop_limit: int) -> Recommendation | None:
    """Suggest that the user set our suggested hop limit."""
    if hop_limit != 3:
        return Recommendation(
            message=f"We recommend a hop limit of 3 vs your current value of {hop_limit}.",
            severity=RecommendationSeverity.WARNING,
        )


def _check_device_role(role: int) -> Recommendation | None:
    """Ensure that the user isn't using a node role that we discourage."""
    discouraged_roles = [
        config_pb2.Config.DeviceConfig.Role.ROUTER,
        config_pb2.Config.DeviceConfig.Role.ROUTER_CLIENT,
        config_pb2.Config.DeviceConfig.Role.REPEATER,
    ]
    if role in discouraged_roles:
        role_name = config_pb2.Config.DeviceConfig.Role.Name(role)
        return Recommendation(
            message=f"Please do not use the {role_name} node role. "
            "Consider CLIENT or CLIENT_MUTE instead.",
            severity=RecommendationSeverity.ERROR,
        )


def _check_module_telemetry_update_interval(
    telemetry_type: str,
    update_interval: int,
) -> Recommendation | None:
    """Suggest that the user keep telemetry intervals to a reasonable level."""
    if update_interval and update_interval < 3600:
        return Recommendation(
            message=f"To help us reduce mesh congestion, lower your {telemetry_type} "
            f"telemetry update interval from {update_interval} to 3600 seconds.",
            severity=RecommendationSeverity.WARNING,
        )


def _check_node_firmware_version(
    node_firmware_version: "firmware_versions.FirmwareVersion",
    latest_firmware_version: "firmware_versions.FirmwareVersion",
) -> Recommendation | None:
    """Ensure that the user is on a current firmware version."""
    if node_firmware_version < latest_firmware_version:
        return Recommendation(
            message=f"To ensure a healthy mesh, please upgrade to the latest"
            f"Meshtastic firmware version ({latest_firmware_version}).",
            severity=RecommendationSeverity.ERROR,
        )


def _check_channels_mqtt_settings(
    channels: list[channel_pb2.Channel] | None,
) -> Recommendation | None:
    """Ensure that the user has not set the dreaded downlink_enable to True."""
    if not channels:
        # Unclear on when this won't be set, but apparently it's not a given!
        return
    for channel in channels:
        if not channel.settings.downlink_enabled:
            return
        channel_index = channel.index
        channel_name = channel_pb2.Channel.Role.Name(channel.role)
        return Recommendation(
            message=f"Disable MQTT uplink on channel {channel_index}: {channel_name}.",
            severity=RecommendationSeverity.ERROR,
        )


def render_validation_report(report: "Report"):
    """Renders the validation report for consumption by the user."""
    success_msg = "Your node is compliant with all Meshtastic Bay Area Group standards!"
    if not report.list_recommendations():
        echo.success(success_msg)
        return

    for recommendation in report.recommendations:
        echo_func = echo._recommendation_severity_to_echo(recommendation.severity)
        echo_func(f"{recommendation.severity.name}: {recommendation.message}")

    if report.validation_successful():
        echo.success(f"{success_msg} Please consider the above warning(s).")
    else:
        echo.error(
            "Your node is not compliant with Meshtastic Bay Area Group standards "
            "due to the above error(s)."
        )
