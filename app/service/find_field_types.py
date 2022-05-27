from typing import Optional


def find_field_types(tree: dict, leaves: Optional[dict] = None, curr_path: Optional[str] = None) -> dict:
    """
    Basically performing DFS here
    """

    if leaves is None:
        leaves = {}

    for key in tree:
        if isinstance(tree[key], dict):
            if "properties" in tree[key]:
                find_field_types(tree[key]["properties"], leaves, key if curr_path is None else f"{curr_path}.{key}")
                tree[key].pop("properties")
            find_field_types(tree[key], leaves, key if curr_path is None else f"{curr_path}.{key}")

        else:
            if key == "type":
                leaves[curr_path] = tree[key]

    return leaves
