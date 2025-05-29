FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install minimal dependencies
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    && pip install --upgrade pip


# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 7860

# Run the application
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
