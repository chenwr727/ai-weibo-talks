from functools import lru_cache

import toml


@lru_cache(maxsize=1)
def load_config():
    return toml.load("./config.toml")
