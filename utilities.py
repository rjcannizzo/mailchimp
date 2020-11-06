"""

"""
import json
from pathlib import Path

HOME_DIR = Path(__file__).resolve().parent


def get_config_file(config_file=Path.home().joinpath('Documents/_rc/mc_config.json')):
    """
    Return a json object with configuation information.
    :param config_file: path to the config file
    :return:json object
    """
    with open(config_file) as f:
        return json.load(f)


def write_to_json_file(out_file, obj):
    with open(out_file, 'w') as f:
        json.dump(obj, f, indent=4)


def get_json_from_file(file_name):
    with open(file_name) as f:
        return json.load(f)


def main():
    pass


if __name__ == '__main__':
    main()
