import logging

def setup_logger(name="finance_analyzer"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # add a file handler if needed
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
