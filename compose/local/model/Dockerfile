FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements /requirements
RUN pip install -r /requirements/model.txt

COPY ./compose/local/model/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app