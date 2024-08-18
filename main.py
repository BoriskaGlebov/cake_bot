# Основной скрипт запуск бота
# import asyncio
import logging
from logging import config
from config_data.logger_config import *
# from tg_api.bot import main
# import sys
import traceback

logger = logging.getLogger('main')
sys.excepthook = any_exception
logging.config.dictConfig(dict_config)
if __name__ == "__main__":
    logger.info('Запуск боту')
    asyncio.run(main())
