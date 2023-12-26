# Stage 1: Python dependencies
FROM python:3.9-alpine as base

WORKDIR /app

# Install git
RUN apk update && apk add --no-cache git

# Clone the repository
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