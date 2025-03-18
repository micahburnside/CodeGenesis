# logger.py

import logging
import sys

def setup_logger(log_file="codegenesis.log"):
    """Setup logging to file and console."""
    logger = logging.getLogger("CodeGenesis")
    logger.setLevel(logging.DEBUG)

    # File handler (detailed logs)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Console handler (info and above)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

logger = setup_logger()
