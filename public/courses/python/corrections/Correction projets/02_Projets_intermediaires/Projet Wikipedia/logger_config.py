import logging

def get_logger():
    logger = logging.getLogger("wiki-analyzer")
    logger.setLevel(logging.DEBUG)

    # Format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler (DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # File handler (INFO+)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Attach handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
