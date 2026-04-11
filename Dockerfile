FROM python:3.10-slim

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir openenv pydantic

# CRITICAL: Tell Python to look in the /app folder for models.py
ENV PYTHONPATH=/app

# Use the Hugging Face port
EXPOSE 7860

# Start the server
CMD ["python", "-m", "openenv.server", "env:EVChargingEnv", "--host", "0.0.0.0", "--port", "7860"]