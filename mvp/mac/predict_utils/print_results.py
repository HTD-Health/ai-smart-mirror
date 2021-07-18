# Imports python modules
import json


def print_results(top_p: list, top_class: list, category_names: str) -> None:
    """
    Print prediction.

    Args:
        top_p (list):
        top_class (list):
        category_names (str): path to file with category names.
    """
    # Load classes classifier will use
    with open(category_names, 'r') as f:
        mask_no_mask = json.load(f)
        
    index = 0
    for elem in top_class:
        mask_state = "yes"
        if "no_mask" in {mask_no_mask[str(int(elem))]}:
            mask_state = "no"

        print(f"Mask on face: {mask_state}")
        print(f"How sure I am: {top_p[index]*100:.0f}%")
        index += 1
