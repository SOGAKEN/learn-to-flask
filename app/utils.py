import logging

import toml


def load_prompts_config(file_path):
    try:
        with open(file_path, "r") as config_file:
            return toml.load(config_file)
    except Exception as e:
        logging.error(f"Failed to load PROMPTS configuration: {e}")
        raise RuntimeError(f"Failed to load configuration from {file_path}")
