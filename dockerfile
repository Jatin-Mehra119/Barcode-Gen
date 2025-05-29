FROM python:3.12.10-alpine

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 7860

# Run the application
CMD ["python", "-m", "streamlit", "run", "streamlit_barcode_app.py", "--server.port=7860", "--server.address=0.0.0.0"]