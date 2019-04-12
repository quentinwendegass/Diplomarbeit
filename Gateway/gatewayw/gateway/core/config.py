import configparser
import os
from gateway.utils import logger, AnsiEscapeSequence

config = None
apn_config_path = None


def get_config():
    return config


def get_apn_config_path():
    return apn_config_path


def set_config(path):
    logger.info('Gateway', 'Using config path: {}{}{}'
                .format(AnsiEscapeSequence.HEADER, path, AnsiEscapeSequence.DEFAULT))
    global config
    global apn_config_path
    config = configparser.ConfigParser()
    config.read(path)
    apn_config_path = os.path.join(os.path.dirname(path), config['DEFAULT']['apnfile'])


