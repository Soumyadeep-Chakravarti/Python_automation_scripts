import logging

# Configure the logger
logging.basicConfig(
    filename='logger.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(error_message):
    logging.error(error_message)

# Example usage
try:
    # Simulate an error
    1 / 0
except Exception as e:
    log_error(f"An error occurred: {e}")