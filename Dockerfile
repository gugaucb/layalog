FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing bytecode and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8100

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install local package in editable or standard mode if needed
RUN pip install --no-cache-dir -e .

EXPOSE 8100

CMD ["python", "run.py"]
