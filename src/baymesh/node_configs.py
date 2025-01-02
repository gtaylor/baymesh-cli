"""Node configuration parser and data structures."""

from typing import List, Self
from dataclasses import dataclass

import pydantic


class BaymeshConfig(pydantic.BaseModel):
    """Python representation of a baymesh.yaml config."""

    nodes: List["LocalNodeConfig"]

    model_config = pydantic.ConfigDict(extra="forbid")

    def list_node_configs(self) -> List["LocalNodeConfig"]:
        """Returns all node configurations."""
        return self.nodes

    def get_node_config_by_alias(self, alias: str) -> "LocalNodeConfig":
        for node_config in self.list_node_configs():
            if node_config.alias == alias:
                return node_config
        raise ValueError(f"Node with alias {alias} not found.")


@dataclass
class LocalNodeConfig(pydantic.BaseModel):
    """Contains the node configs that the user expects to be present or applied."""

    alias: str
    address: str | None = None
    dev_path: str | None = None

    @pydantic.model_validator(mode="after")
    def check_connection_configs(self) -> Self:
        """Validates that the user provided only one connection config."""
        connection_values = (self.address, self.dev_path)
        if all(connection_values):
            raise ValueError(
                "Node configs must provide values for *only* one of address or dev_path."
            )
        if not any(connection_values):
            raise ValueError(
                "Node configs must provide values for one of address or dev_path."
            )
        return self
