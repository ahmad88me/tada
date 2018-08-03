import logging


def set_config(logger, extra=""):
    if extra != "":
        extra = "-" + extra
    handler = logging.FileHandler('tada%s.log' % extra)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
