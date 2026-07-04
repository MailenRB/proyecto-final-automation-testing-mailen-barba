import logging
import os

def get_logger(name):
    """
    Creates or retrieves a logger configured to write to console and a file.
    """
    logger = logging.getLogger(name)
    # Prevent duplicate handlers if the logger is retrieved multiple times
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Dynamically resolve the logs directory relative to this utility's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(current_dir, "..", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        log_file = os.path.join(logs_dir, "execution.log")
        
        # Formatting pattern
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler for local logs persistency
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler to output logs to test runners
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
