import json

DEFAULT_CONFIG_PATH = "config.json"


def load_config_file(config_json_path: str = DEFAULT_CONFIG_PATH) -> dict:
    """
    Load data stored in file build in JSON schema into dictionary.

    Args:
        config_json_path (str):

    Returns:
        (dict): configuration data stored in dictionary.
    """
    # Opening JSON file
    with open(config_json_path) as json_file:
        config_data = json.load(json_file)
    return config_data
