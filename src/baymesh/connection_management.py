"""Device connection management logic."""

import typing

import meshtastic
import meshtastic.serial_interface
import serial.tools.list_ports

if typing.TYPE_CHECKING:
    from serial.tools.list_ports_common import ListPortInfo


def detect_supported_devices_via_serial() -> list["ListPortInfo"]:
    """Returns a list of ports that may have a supported device connected."""
    supported_devices = meshtastic.util.detect_supported_devices()
    if not supported_devices:
        return []
    candidate_ports = meshtastic.util.active_ports_on_supported_devices(supported_devices)
    all_serial_ports = serial.tools.list_ports.comports()
    matches = []
    for serial_port in all_serial_ports:
        if serial_port.device in candidate_ports:
            matches.append(serial_port)
    return matches
