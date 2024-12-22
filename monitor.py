import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# JSON log dosyası yolu
LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("modified", event.src_path)

    def on_created(self, event):
        self.log_event("created", event.src_path)

    def on_deleted(self, event):
        self.log_event("deleted", event.src_path)

    def log_event(self, action, path):
        log_entry = {
            "action": action,
            "path": path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(LOG_FILE, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

if _name_ == "_main_":
    # İzlenecek dizin
    watch_directory = "/home/ubuntu/bsm/test"
    observer = Observer()
    event_handler = ChangeHandler()

    # İzleyici başlat
    observer.schedule(event_handler, watch_directory, recursive=True)
    observer.start()
    print(f"Monitoring changes in: {watch_directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()