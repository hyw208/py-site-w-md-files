import time
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the minimum level to log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log format
    datefmt='%Y-%m-%d %H:%M:%S',  # Specify the date format
)

logging.Formatter.converter = time.gmtime  # Ensures UTC time is used

def getLogging():
    return logging