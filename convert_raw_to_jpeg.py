import os
import time
import rawpy
import imageio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "/usr/src/app/upload"
target_dir = "/usr/src/app/converted"

RAW_EXTENSIONS = ['.arw', '.dng', '.gpr']

def log_status(message):
    """
    Utility function to log a status message with separators.
    """
    print(f"\n{'=' * 40}\n\n{message}\n\n{'=' * 40}\n")

def is_raw_file(file_name):
    """
    Checks if a file has a supported RAW extension.
    """
    return any(file_name.lower().endswith(ext) for ext in RAW_EXTENSIONS)

import numpy as np

def process_raw_file(raw_path):
    """
    Processes a single RAW file and converts it to a high-quality JPEG.
    """
    filename = os.path.splitext(os.path.basename(raw_path))[0]
    output_path = os.path.join(target_dir, f"{filename}.jpeg")

    if os.path.exists(output_path):
        print(f"✔ Skipping {raw_path} - {output_path} already exists.")
        return

    try:
        print(f"🛠 Starting conversion: {raw_path} -> {output_path}")
        
        with rawpy.imread(raw_path) as raw:
            rgb = raw.postprocess(
                use_camera_wb=True,              # Use camera's white balance
                no_auto_bright=True,             # Prevent auto-brightness adjustments
                output_bps=16,                   # 16-bit output for better precision
                demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD,  # High-quality demosaic
                gamma=(2.2, 4.5),                # Gamma correction for natural contrast
                chromatic_aberration=(1.0, 1.0), # Reduce chromatic aberration
                noise_thr=100,                   # Basic noise reduction threshold
                median_filter_passes=1,          # Apply a median filter for noise removal
            )

        # Convert 16-bit RGB image to 8-bit for JPEG compatibility
        rgb_8bit = np.clip(rgb / 256, 0, 255).astype(np.uint8)

        imageio.imwrite(output_path, rgb_8bit, format="JPEG", quality=98)
        print(f"✅ Successfully converted: {raw_path} -> {output_path}")

    except Exception as e:
        print(f"❌ Error converting {raw_path}: {e}")

def scan_and_process_directory():
    """
    Scans the source directory and processes all RAW files.
    """
    log_status("Scanning source directory for RAW files...")
    files_converted = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if is_raw_file(file):
                raw_path = os.path.join(root, file)
                process_raw_file(raw_path)
                files_converted += 1

    if files_converted == 0:
        print("✨ No new files to convert. All files are up-to-date.")

class FileChangeHandler(FileSystemEventHandler):
    """
    Event handler for file changes in the source directory.
    """
    def on_any_event(self, event):
        if event.is_directory:
            return

        # Trigger conversion only if a RAW file is modified or added
        if is_raw_file(event.src_path):
            log_status(f"🛎 Change detected: {event.src_path}")
            scan_and_process_directory()

if __name__ == "__main__":
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Initial scan and process
    log_status(f"🚀 Initial processing from {source_dir} to {target_dir}...")
    scan_and_process_directory()

    # Start monitoring the source directory for changes
    log_status(f"👀 Monitoring directory: {source_dir}")
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_dir, recursive=True)

    try:
        observer.start()
        while True:
            print("✨ Waiting for file changes...")
            time.sleep(5)  # Idle log every 5 seconds
    except KeyboardInterrupt:
        observer.stop()
        log_status("🛑 Monitoring stopped. Exiting gracefully...")

    observer.join()
