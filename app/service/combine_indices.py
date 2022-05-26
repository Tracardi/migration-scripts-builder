
def combine_indices(old_indices: dict, new_indices: dict) -> dict:

    common_indices = set(old_indices.keys()).intersection(set(new_indices.keys()))

    return {
        index_name: {"old": old_indices[index_name], "new": new_indices[index_name]} for index_name in common_indices
    }



