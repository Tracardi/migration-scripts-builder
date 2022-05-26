from deepdiff import DeepDiff
from deepdiff.model import PrettyOrderedSet
import re


def find_mappings_difference(old_indices: dict, new_indices: dict) -> dict:

    common_indices = set(old_indices.keys()).intersection(set(new_indices.keys()))

    combined = {
        re.split(r"-[0-9]{4}-[0-9]", index_name)[0]: {
            "old": old_indices[index_name], "new": new_indices[index_name]
        } for index_name in common_indices
    }

    for index_name in combined:
        diff = DeepDiff(combined[index_name]["old"]["mappings"], combined[index_name]["new"]["mappings"])
        combined[index_name] = diff if diff else None

    result = {key: combined[key] for key in combined if combined[key] is not None}

    for index_name in result:
        for key in result[index_name]:

            if isinstance(result[index_name][key], PrettyOrderedSet):
                result[index_name][key] = [
                    ".".join([key[2:-2] for key in re.findall(r"\['[a-z _]{1,}']", element)[1:]])
                    for element in result[index_name][key]
                ]

            elif isinstance(result[index_name][key], dict):
                result[index_name][key] = {
                    ".".join([key[2:-2] for key in re.findall(r"\['[a-z _]{1,}']", field)[1:]]):
                        result[index_name][key][field]
                    for field in result[index_name][key]
                }

    return result

