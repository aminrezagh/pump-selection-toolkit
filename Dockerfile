# Stage 1: Python dependencies
FROM python:3.9-slim-bullseye as base

WORKDIR /app

# Clone the repository and install the dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    curl -SL https://github.com/aminrezagh/pump-selection-toolkit.git | tar xz --strip-components=1 && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Copy application code
FROM base as source

COPY . .

# Stage 3: Run the application
FROM source as final

# Remove unnecessary files and directories
RUN apt-get purge -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Streamlit uses this port
EXPOSE 8501

# The command to run the application
CMD ["streamlit", "run", "01  🗺️ Dashboard.py"]