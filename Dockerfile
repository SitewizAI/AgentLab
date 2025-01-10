FROM python:3.11

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    xvfb \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install AgentLab
COPY . .
RUN pip install -e .

# Install Playwright with all dependencies
RUN playwright install chromium --with-deps

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AGENTLAB_EXP_ROOT=/data/agentlab_results
ENV DISPLAY=:99

# Create volume mount point
VOLUME /data

EXPOSE 8000

# Start Xvfb and the application
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & uvicorn main:app --host 0.0.0.0 --port 8000"]