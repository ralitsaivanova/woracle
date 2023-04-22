import logging

import os
import sys

sys.path.append(os.getcwd())

from cakeshop.db import engine
from cakeshop.db.base_class import Base
from cakeshop.db.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Creating table")
    Base.metadata.create_all(bind=engine)
    logger.info("Table created")
