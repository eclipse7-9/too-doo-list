FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
# Install system build dependencies required by some Python packages (cryptography)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   libssl-dev \
	   libffi-dev \
	   python3-dev \
	   cargo \
	&& python -m pip install --upgrade pip setuptools wheel \
	&& pip install --no-cache-dir -r requirements.txt \
	&& apt-get remove -y build-essential python3-dev cargo \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Ensure logs are shown immediately
ENV PYTHONUNBUFFERED=1

# Default port - Railway provides $PORT at runtime; fall back to 8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
