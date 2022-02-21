import logging
import os
import datetime


if not os.path.exists(os.path.join("output", datetime.datetime.now().strftime('%Y%m%d%H%M%S'))):
    os.makedirs(os.path.join(
        "output", datetime.datetime.now().strftime('%Y%m%d%H%M%S')))

logger = logging.getLogger("client_log")

logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
log_file_handler = logging.FileHandler(filename=os.path.join(
    "output", datetime.datetime.now().strftime('%Y%m%d%H%M%S'), "seaport.log"), encoding="utf-8")

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(message)s")

stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
log_file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(log_file_handler)
