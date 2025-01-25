import os
from dataclasses import dataclass
from pathlib import Path

import rich
import yaml


@dataclass
class Config:

    api_key: str

    @property
    def key(self):
        return self.api_key

    def to_dict(self):
        return {"apiKey": self.api_key}

def does_config_file_exist(filepath: str = ".config/ace/config.yaml") -> bool:
    """
    Check if the configuration file with containing a given api key already exists.
    :return: bool based on result of looking for file
    """
    config_file_path = Path(f"{Path.home()}/{filepath}")
    if config_file_path.is_file():
        print(f"Configuration file {config_file_path} exists")
        return True
    print(f"Configuration file {config_file_path} does not exist")
    return False


def get_config(filepath: str = f"{Path.home()}/.config/ace/config.yaml") -> Config:
    """
    Will return the configuration file as config object
    :param filepath: get the configuration from a given file
    :return: yaml mapped into configuration object
    """
    with open(filepath, "r") as stream:
        try:
            return Config(yaml.safe_load(stream)["apiKey"])
        except yaml.YAMLError as exc:
            rich.print(f"Error occurred whilst parsing configuration file: {exc}")

def write_config_file(filepath: str, api_key: str) -> bool:
    """
    Will write a new configuration file, should only call this method when a configuration file is not found, if called
    repeatedly will end up with multiple configuration files.
    :param api_key: api_key for the weather api and will write this to the file
    :param filepath: filepath to write configuration file to
    :return: boolean based on result of writing file
    """
    full_path = os.path.join(filepath, "config.yaml")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as stream:
        try:
            # print(f"Writing configuration file: {filepath}/config.yaml")
            yaml.dump(Config(api_key=api_key).to_dict(), stream, default_flow_style=False)
            return True
        except yaml.YAMLError as exc:
            rich.print(f"Error occurred whilst writing configuration file: {exc}")
            return False

def initialize_config(api_key: str) -> Config:
    """
    Initializes a new configuration file and will allow the user to create a file at a path of their choosing
    :param api_key: api_key for the weather api and will write this to the file
    :return: Config object containing the key alongside the configuration file
    """
    filepath = f"{Path.home()}/.config/ace"
    result: bool = write_config_file(filepath, api_key)
    if result:
        return Config(api_key=api_key)
    else:
        rich.print(f"Failed to write a new configuration file at: {filepath}")
