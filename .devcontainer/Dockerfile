FROM python:3.12-slim

# Create a non-root user (optional, but recommended)
RUN useradd -ms /bin/bash vscode

# Install common packages
RUN apt-get update && apt-get install -y \
    git curl build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace