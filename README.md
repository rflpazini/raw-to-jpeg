# RAW-to-JPEG Converter [![Build](https://github.com/rflpazini/raw-to-jpeg/actions/workflows/build.yml/badge.svg)](https://github.com/rflpazini/raw-to-jpeg/actions/workflows/build.yml)

A Python-based tool that monitors a folder for RAW image files, converts them to JPEG format, and saves them in a target directory. The tool supports popular RAW formats like `.arw`, `.dng`, and `.gpr` and uses Docker for easy deployment.


## Features
- 🚀 Automatic Monitoring: Continuously watches a folder for new RAW files.
- 🔄 On-the-Fly Conversion: Converts RAW files (e.g., .arw, .dng, .gpr) to high-quality JPEG format.
- 📂 Organized Output: Saves converted files to a dedicated target folder.
- 🐳 Dockerized Deployment: Easily run the tool using Docker.
- ✅ Idempotent Processing: Skips files that are already converted.
- 📜 Real-Time Logs: Displays detailed logs for conversions and folder monitoring.

## How It Works

The script scans a source folder for RAW files.
It processes supported RAW formats (e.g., .arw, .dng) and converts them into JPEG images.
The converted images are saved in a target folder.
The script continuously monitors the source folder for new or modified files.

## Requirements
To run this project locally or in Docker, you need:

- Python: 3.8+
- Libraries: [rawpy](https://pypi.org/project/rawpy/), [imageio](https://pypi.org/project/imageio/), [watchdog](https://pypi.org/project/watchdog/)
- Docker (optional for containerized execution)

## Project Structure

```bash
raw-to-jpeg/
│
├── convert_raw_to_jpeg.py   # Main Python script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image configuration
└── docker-compose.yml       # Docker Compose setup
```

## Installation and Usage

1. Clone the Repository
```bash
git clone https://github.com/rflpazini/raw-to-jpeg.git
cd raw-to-jpeg
```

2. Install Dependencies Locally
```bash
pip install -r requirements.txt
```

3. Run the Script
Set up the source and target folders:
```bash
export SOURCE_DIR=~/Downloads/ph_raw
export TARGET_DIR=~/Downloads/ph_converted

python convert_raw_to_jpeg.py
```

## Contributing
Contributions are welcome! Here's how you can contribute:

- Fork the repository.
- Create a new branch for your feature:
```bash
git checkout -b feature-new-enhancement
```
- Commit your changes and submit a pull request.

## License
This project is licensed under the MIT License. See [License](http://rflpazini.mit-license.org) for details.
