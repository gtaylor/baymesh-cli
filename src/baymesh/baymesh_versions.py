"""Checks to make sure that the user has the latest version of the CLI installed."""

import requests

from baymesh import __version__


def _version_from_pypi_url(url: str) -> str:
    """Given a PyPi source archive URL, return the package's version number."""
    source_archive_name = url.split("/")[-1]
    return source_archive_name.lstrip("baymesh-").rstrip(".tar.gz")


def get_latest_version() -> str:
    """Returns the latest version of the CLI available in PyPi."""
    try:
        response = requests.get("https://pypi.org/pypi/baymesh/json", timeout=3)
    except requests.exceptions.RequestException as exception:
        raise RuntimeError(f"Failed to get latest version from PyPi, {exception}")
    rdict = response.json()
    # Example JSON output: https://pypi.org/pypi/baymesh/json
    # urls keyword seems to be sorted and there is a wheel and a tarball per version.
    for url in rdict["urls"][-2:]:
        if url["url"].endswith(".tar.gz"):
            return _version_from_pypi_url(url["url"])
    raise RuntimeError("Unable to find the latest version of baymesh CLI.")


def get_current_version() -> str:
    """Returns the installed version of the CLI."""
    return __version__


def is_up_to_date() -> tuple[bool, str]:
    """Returns a Tuple of version info.

    Tuple is in the form of (<is_up_to_date>, <current_version>).
    """
    latest_version = get_latest_version()
    installed_version = get_current_version()
    up_to_date = latest_version == installed_version
    return up_to_date, latest_version
