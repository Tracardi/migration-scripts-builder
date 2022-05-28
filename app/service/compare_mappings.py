from dotty_dict.dotty_dict import Dotty


def compare_mappings(old_mapping: dict, new_mapping: dict) -> dict:
    removed = set(old_mapping) - set(new_mapping)
    added = set(new_mapping) - set(old_mapping)

    type_changes = {
        key: {"old": old_mapping[key], "new": new_mapping[key]} for key in old_mapping if
        key in old_mapping and
        key in new_mapping and
        old_mapping[key] != new_mapping[key]
    }

    return {
        "removed": list(removed),
        "added": list(added),
        "type_changes": type_changes
    }
