import logging
import os

import toml


def load_prompts():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        toml_path = os.path.join(script_dir, "..", "prompts.toml")
        with open(toml_path, "r") as f:
            prompts = toml.load(f)
        logging.info(f"Successfully loaded prompts: {prompts}")
        return prompts
    except Exception as e:
        logging.error(f"Error loading prompts.toml: {e}")
        return {}
