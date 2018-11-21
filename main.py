import logging
import os
import shelve

import yaml
from soroush_python_sdk import Client

import admin_commands
import config
import logging.config

from quran import start_bot


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = os.path.join(os.path.dirname(__file__), default_path)
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        logging.warning("log config doesn't detected. using defaults")
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('sseclient').setLevel(logging.INFO)

def main():
    try:
        bot = Client(config.bot_token)
        res = shelve.open('medias.dbm')
        logging.info('starting bot...')
        admin_commands.bot_start_report(bot, res=res)
        start_bot(bot, res)
    except Exception as e:
        logging.exception('Bad things happend!')
        try:
            for admin in config.bot_admins:
                bot.send_text(admin, str(e))
        except Exception:
            pass
    finally:
        res.close()


if __name__ == '__main__':
    setup_logging()
    main()
