"""Firmware version munging."""

import io
import typing
import functools
import dataclasses
import contextlib

import requests

if typing.TYPE_CHECKING:
    import meshtastic  # pyright: ignore [reportMissingTypeStubs]


@functools.total_ordering
@dataclasses.dataclass
class FirmwareVersion(object):
    """Internal representation of a Meshtastic firmware version."""

    major: int
    minor: int
    patch: int
    commit_hash: str

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}.{self.commit_hash}"

    def __eq__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.as_tuple() == other.as_tuple()

    def __gt__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        if self.major > other.major:
            return True
        if self.major >= other.major and self.minor > other.minor:
            return True
        if (
            self.major >= other.major
            and self.minor >= other.minor
            and self.patch >= other.patch
        ):
            return True
        return False

    @staticmethod
    def _is_valid_operand(other) -> bool:
        """Determines whether the other object is comparable."""
        return (
            hasattr(other, "major")
            and hasattr(other, "minor")
            and hasattr(other, "patch")
            and callable(getattr(other, "as_tuple"))
        )

    def as_tuple(self) -> "typing.Tuple[int, int, int, str]":
        """Returns a tuple of all version elements."""
        return self.major, self.minor, self.patch, self.commit_hash


def _parse_firmware_version_str(firmware_str: str) -> FirmwareVersion:
    """Parses a Meshtastic firmware version string and returns a FirmwareVersion."""
    version_split: list[str] = firmware_str.split(".")
    return FirmwareVersion(
        major=int(version_split[0]),
        minor=int(version_split[1]),
        patch=int(version_split[2]),
        commit_hash=version_split[3],
    )


def get_node_firmware_version(node: "meshtastic.Node") -> FirmwareVersion:
    """Retrieves the connected node's firmware version and returns a FirmwareVersion.

    The meshtastic library's Node.getMetadata() function prints out the firmware version
    instead of returning it, so we've got to work around by redirecting stdout.
    """
    output_buf = io.StringIO()
    with contextlib.redirect_stdout(output_buf):
        node.getMetadata()
    output = output_buf.getvalue()
    version_str = output.split("firmware_version: ")[1].split("\n")[0]
    return _parse_firmware_version_str(version_str)


def get_latest_firmware_version() -> FirmwareVersion:
    """Retrieves the latest firmware version from GitHub and returns a FirmwareVersion."""
    response = requests.get(
        "https://api.github.com/repos/meshtastic/firmware/releases/latest"
    )
    release = response.json()
    tag_name = release["tag_name"]
    # The upstream git tags have a "v" prefix that we need to remove for consistency.
    version_str = tag_name.lstrip("v")
    return _parse_firmware_version_str(version_str)
