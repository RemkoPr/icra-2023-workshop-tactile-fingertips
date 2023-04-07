import os
import sys
from absl import app
from absl import flags
from loguru import logger
import asyncio

from utils.builder import Builder

FLAGS = flags.FLAGS


def main(_):
    ARDUINO1 = "C2:55:80:51:13:5C"

    # only log at INFO level to console
    logger.configure(handlers=[{"sink": sys.stderr, "level": "DEBUG"}])
    logger.add(os.path.join('./data', "irtouch32_textile.log"), rotation="500 MB", level="DEBUG")

    devices = [ARDUINO1]
    sensors = Builder.irtouch32(devices=devices, data_directory='./data/irtouch', comm_mode="BLEAK")

    asyncio.get_event_loop().run_until_complete(sensors.subscribe_to_devices(visualiser_delay=0.01))


if __name__ == '__main__':
    app.run(main)
