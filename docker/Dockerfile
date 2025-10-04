# Base image and dependency installation template for the LLogM prototype.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/workspace/.cache/huggingface

WORKDIR /workspace

# TODO: install system dependencies (git, gcc, java, etc.) and Python requirements.
COPY requirements.txt constraints.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt -c constraints.txt

COPY . .

CMD ["bash"]
