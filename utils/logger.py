import logging

def get_logger(name="pla2049"):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
