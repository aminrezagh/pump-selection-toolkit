# Stage 1: Python dependencies
FROM python:3.9-slim as base

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/aminrezagh/pump-selection-toolkit.git .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Copy application code
FROM base as source

COPY . .

# Stage 3: Run the application
FROM source as final

# Streamlit uses this port
EXPOSE 8501

# The command to run the application
CMD ["streamlit", "run", "01 🗺️ Dashboard.py"]