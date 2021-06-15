import logging


def get_logger(logger_name, filename):
    base_level = logging.INFO

    handler = logging.FileHandler(filename, mode='a+', encoding='UTF-8')
    handler.setLevel(base_level)

    logger = logging.getLogger(logger_name)
    logger.setLevel(base_level)
    logger.addHandler(handler)

    return logger
