import time 
import os
from dotenv import load_dotenv
import shutil
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

load_dotenv()
WATCH_DIR = os.getenv("WATCH_DIR")