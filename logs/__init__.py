import os
import logging
from logging.handlers import RotatingFileHandler
from conf import ConfManagement


class DevelopmentConfig(object):
    DEBUG = ConfManagement("default").get_ini("DEBUG")
    LOG_LEVEL = logging.DEBUG


class SetLog(object):

    def setup_log(e):
        logging.basicConfig(level=DevelopmentConfig.LOG_LEVEL)
        log_path = os.path.dirname(os.path.realpath(__file__))
        log = os.path.join(log_path, "project.log")
        file_log_handler = RotatingFileHandler(
            log, maxBytes=1024 * 1024 * 100, backupCount=10)
        # formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(levelname)s %(name)s:%(lineno)d %(message)s')
        file_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_log_handler)

    def __getattr__(self, e):
        self.setup_log()
        log_match = {
            "info": logging.info,
            "debug": logging.debug,
            "error": logging.error,
            "warning": logging.warning
        }
        if e in log_match.keys():
            return log_match.get(e)
