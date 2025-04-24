FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install Python packages
# COPY backend/requirements.txt ./

# RUN pip install -r requirements.txt
RUN pip install --upgrade pip

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY backend .

RUN cd /app && pip install -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
