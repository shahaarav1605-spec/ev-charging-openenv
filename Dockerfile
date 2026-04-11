# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# VERY IMPORTANT: set PYTHONPATH
ENV PYTHONPATH=/app

# Run correct server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]