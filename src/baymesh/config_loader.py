"""Node configuration loading logic."""

import yaml

from baymesh import node_configs


def load_from_file(config_path: str) -> node_configs.BaymeshConfig:
    """Loads and returns a parsed BaymeshConfig from a file."""
    with open(config_path, "rb") as fobj:
        return load(fobj.read())


def load(config_contents: bytes) -> node_configs.BaymeshConfig:
    """Loads and returns a parsed BaymeshConfig from bytes."""
    data = yaml.load(config_contents, Loader=yaml.Loader)
    return node_configs.BaymeshConfig(**data)
