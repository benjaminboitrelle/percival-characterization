import os
import sys

try:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
except:
    CURRENT_DIR = os.path.dirname(os.path.realpath('__file__'))

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
SRC_PATH = os.path.join(BASE_PATH, "src")
PROCESS_PATH = os.path.join(SRC_PATH, "process")

if PROCESS_PATH not in sys.path:
    sys.path.insert(0, PROCESS_PATH)
