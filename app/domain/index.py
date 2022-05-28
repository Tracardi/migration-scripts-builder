from pydantic import BaseModel
from typing import Dict, Optional, Any


class Index(BaseModel):
    name: str
    multi: bool
    mapping: Dict[str, Any] = {}

    @staticmethod
    def standardize_mapping(mappings: dict, curr_path: str = None, fields: dict = None) -> dict:
        if fields is None:
            fields = {}

        for key in mappings:
            if isinstance(mappings[key], dict) and "properties" in mappings[key]:
                Index.standardize_mapping(
                    mappings[key]["properties"],
                    key if curr_path is None else f"{curr_path}.{key}",
                    fields
                )

            if "type" in mappings[key]:
                fields[key if curr_path is None else f"{curr_path}.{key}"] = mappings[key]["type"]

        return fields

