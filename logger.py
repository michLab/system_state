import logging
import sys
import time

LOGGER_VERSION = 1.0

class Logger:
    def __init__(self, logger_name='__name__', file_name=' ',
                 file_level=-1, console_level=-1,
                 formatter='%(created).6f %(name)-12s %(levelname)-8s %(message)s'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        
        if console_level in {logging.DEBUG, logging.INFO, logging.WARNING,
                logging.ERROR, logging.CRITICAL}:
            self.console_formatter = logging.Formatter(formatter)
            self.console_level = console_level
            self.init_console_handler()
            self.logger.addHandler(self.console_handler)

        if file_name is not ' ' and file_level in {logging.DEBUG,
                logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL}:
            self.file_name = file_name
            self.file_level = file_level
            self.file_formatter = logging.Formatter(formatter)
            self.init_file_handler()
            self.logger.addHandler(self.file_handler)

        self.logger.propagate = False
            

    def init_console_handler(self):
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setFormatter(self.console_formatter)
        self.console_handler.setLevel(self.console_level)
    

    def init_file_handler(self):
        self.file_handler = logging.FileHandler(self.file_name)
        self.file_handler.setFormatter(self.file_formatter)
        self.file_handler.setLevel(self.file_level)


    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)


    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)
    

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
        

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)


    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
