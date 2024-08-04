# watchAndRename.py

# MIT License
# Dennis Cao (dennis-cao-net)


import os
import time
import subprocess
import librosa
import librosa.display
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the folder to watch and output folder
WATCHED_FOLDER = 'Z:\\SongsFromMac'
OUTPUT_FOLDER = 'Z:\\StemsFromPC'

# Determine the path of the current directory and the AHK script
current_directory = os.path.dirname(os.path.abspath(__file__))
AHK_SCRIPT_PATH = os.path.join(current_directory, 'RipX-script.ahk')

class SongProcessor:
    def __init__(self, path):
        self.path = path
        self.key = '??'
        self.bpm = 0
        self.process_song()

    def process_song(self):
        y, sr = librosa.load(self.path)
        self.key = self.detect_key(y, sr)
        self.bpm = self.detect_tempo(y, sr)
        self.rename_file()

    def detect_key(self, y, sr):
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = chroma.mean(axis=1)
        key_index = chroma_mean.argmax()

        # Camelot wheel mapping (A and B for minor and major respectively)
        camelot_wheel = [
            "8B", "3B", "10B", "5B", "12B", "7B", "2B", "9B", "4B", "11B", "6B", "1B",  # Major
            "5A", "12A", "7A", "2A", "9A", "4A", "11A", "6A", "1A", "8A", "3A", "10A"   # Minor
        ]

        # Determine key
        if key_index < len(camelot_wheel):
            key = camelot_wheel[key_index]
        else:
            key = '??'

        return key

    def detect_tempo(self, y, sr):
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return int(tempo)

    def rename_file(self):
        directory, original_filename = os.path.split(self.path)
        basename, ext = os.path.splitext(original_filename)
        new_filename = f"{self.key}_{self.bpm}BPM_{basename}{ext}"
        new_path = os.path.join(directory, new_filename)
        os.rename(self.path, new_path)
        print(f"Renamed '{original_filename}' to '{new_filename}'")

        # Call the AHK script to process the file with RipX DAW
        subprocess.call(['C:\\Program Files\\AutoHotkey\\AutoHotkey.exe', AHK_SCRIPT_PATH])

class Watcher:
    def __init__(self, folder_to_watch):
        self.folder_to_watch = folder_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.folder_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            SongProcessor(event.src_path)

if __name__ == '__main__':
    w = Watcher(WATCHED_FOLDER)
    w.run()
