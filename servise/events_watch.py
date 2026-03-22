import time 
import os
from dotenv import load_dotenv
import shutil
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

load_dotenv()
WATCH_DIR = os.getenv("WATCH_DIR")

class MyHandler(PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(patterns=["*.jpg", "*.jpeg", "*.png"], ignore_directories=True)

    def on_created(self, event):
        file_path = event.src_path
        filename = os.path.basename(file_path)
        print(f"新しいファイルが追加されました: {filename}")

        time.sleep(2)  # ファイルが完全に保存されるのを待つ

        #try: #ここに処理の関数を入れる
            
        ##except Exception as e:
        #    print(f"エラーが発生しました: {e}") 