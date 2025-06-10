
import os
import time
import glob
import logging

# Set up logger for maintenance actions
logging.basicConfig(filename="/var/log/maintenance.log", level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

LOG_FILES = [
    "/var/log/can_logger.log",
    "/var/log/alert_log.txt",
    "/var/log/dtc_log.txt"
]

TEMP_PATTERNS = [
    "/home/pi/*.dump",
    "/home/pi/*.dtc",
    "/home/pi/*.tmp"
]

MAX_LOG_AGE_SECONDS = 7 * 24 * 3600  # 7 days

def clear_all_logs():
    logging.info("Manual log cleanup requested.")
    for path in LOG_FILES:
        try:
            open(path, 'w').close()
            logging.info(f"Cleared log file: {path}")
        except Exception as e:
            logging.error(f"Failed to clear log {path}: {e}")

    for pattern in TEMP_PATTERNS:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                logging.info(f"Deleted temp file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete temp file {file_path}: {e}")

def auto_cleanup_old_logs():
    now = time.time()
    for path in LOG_FILES:
        try:
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                if now - mtime > MAX_LOG_AGE_SECONDS:
                    open(path, 'w').close()
                    logging.info(f"Auto-cleared old log: {path}")
        except Exception as e:
            logging.error(f"Auto-cleanup error on log {path}: {e}")

    for pattern in TEMP_PATTERNS:
        for file_path in glob.glob(pattern):
            try:
                if now - os.path.getmtime(file_path) > MAX_LOG_AGE_SECONDS:
                    os.remove(file_path)
                    logging.info(f"Auto-deleted old temp file: {file_path}")
            except Exception as e:
                logging.error(f"Error deleting {file_path}: {e}")
