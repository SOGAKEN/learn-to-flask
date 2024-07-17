import os

import toml


def load_prompts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    toml_path = os.path.join(script_dir, "..", "prompts.toml")
    with open(toml_path, "r") as f:
        return toml.load(f)


PROMPTS = load_prompts()
