FROM python:3.13-slim AS base
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    SOURCE_DIR=/usr/src/app/upload \
    TARGET_DIR=/usr/src/app/converted

RUN mkdir -p ${SOURCE_DIR} ${TARGET_DIR}

CMD ["python", "convert_raw_to_jpeg.py"]
