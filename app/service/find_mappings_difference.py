from deepdiff import DeepDiff


def find_mappings_difference(combined: dict) -> dict:
    for index_name in combined:
        combined[index_name]["diff"] = DeepDiff(combined[index_name]["old"], combined[index_name]["new"])

    return combined
