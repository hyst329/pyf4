import sys

__author__ = 'main'

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename=sys.argv[1] + ".log",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()