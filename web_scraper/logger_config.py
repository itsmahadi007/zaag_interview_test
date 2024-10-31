# logger_config.py
import logging
from datetime import datetime

# Generate a timestamp string
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Configure the logging
logging.basicConfig(
    filename=f'logs/scraper_{timestamp}.log',  # Log file name with timestamp in logs directory
    level=logging.DEBUG,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

# # Create a logger object
# logger = logging.getLogger(__name__)
