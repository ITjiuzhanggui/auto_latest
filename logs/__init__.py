import os
import logging
import os
from logging.handlers import RotatingFileHandler
from conf import ConfManagement


class DevelopmentConfig(object):
    DEBUG = ConfManagement().get_ini("debug_format")
    log_match = {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "error": logging.ERROR,
        "warning": logging.WARNING
    }
    LOG_LEVEL = log_match.get(DEBUG)


class SetLog(object):

    def setup_log(e):
        logging.basicConfig(level=DevelopmentConfig.LOG_LEVEL)
        log_path = os.path.dirname(os.path.realpath(__file__))
        log = os.path.join(log_path, "project.log")
        file_log_handler = RotatingFileHandler(
<<<<<<< HEAD
            log, maxBytes=1024 * 1024 * 100, backupCount=10)
=======
        log, maxBytes=1024 * 1024 * 100, backupCount=10)
>>>>>>> ae1124d7c678b958082ae4872a55f9e190414c9e
        # formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
