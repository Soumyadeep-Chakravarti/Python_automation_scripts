import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os
import colorlog


class LoggerSetup:
    def __init__(
        self,
        log_dir="logs",
        log_level=logging.DEBUG,
        max_log_size=10 * 1024 * 1024,
        backup_count=5,
    ):
        self.log_dir = log_dir
        self.log_level = log_level
        self.max_log_size = max_log_size
        self.backup_count = backup_count

        # Create log directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Setup the logger
        self.logger = self._configure_logger()

    def _configure_logger(self):
        """
        Configures the logger with rotating file handler, console handler (with colors), and a custom format.
        """
        # Create a custom formatter for file and console logs
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

        # Set up the root logger
        logger = logging.getLogger()  # Root logger
        logger.setLevel(self.log_level)

        # File handler with log rotation
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir, "app.log"),
            maxBytes=self.max_log_size,
            backupCount=self.backup_count,
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

        # Colored console handler (using colorlog for colored output)
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(self.log_level)

        # Define color format for console
        color_format = (
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        color_formatter = colorlog.ColoredFormatter(
            color_format,
            datefmt=date_format,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler.setFormatter(color_formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def get_logger(self, logger_name=None):
        """
        Returns a logger instance. If a logger_name is provided, it will return a named logger.
        """
        if logger_name:
            return logging.getLogger(logger_name)
        return self.logger

    def log_exception(self, logger, exception, message="An error occurred"):
        """
        Logs an exception with a traceback.
        """
        logger.error(f"{message}: {exception}", exc_info=True)


# Example of usage:
if __name__ == "__main__":
    # Initialize the logger setup
    log_setup = LoggerSetup(log_dir="logs", log_level=logging.DEBUG)

    # Get the root logger
    logger = log_setup.get_logger()

    # Log some messages
    # logger.debug('Debug message: Everything is running fine.')
    # logger.info('Info message: Process started successfully.')
    # logger.warning('Warning message: A non-critical issue occurred.')
    # logger.error('Error message: Something went wrong.')
    # logger.critical('Critical message: Immediate action required.')

    # Simulate an exception
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        log_setup.log_exception(logger, e, "Error during division operation")
