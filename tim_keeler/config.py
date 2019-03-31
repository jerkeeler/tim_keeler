import os
from typing import Dict

import toml

CONF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf')
CONF_EXTENSION = '.toml'

_conf_cache = {}


def load_conifg(config_name: str) -> Dict:
    config_name += CONF_EXTENSION
    config = toml.load(os.path.join(CONF_DIR, config_name))
    _conf_cache[config_name] = config
    return config


def get_config(config_name: str) -> Dict:
    return _conf_cache.get(config_name, load_conifg(config_name))
