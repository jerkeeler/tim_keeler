import logging.config

from tim_keeler.config import get_config

logging.config.dictConfig(get_config('logging'))
