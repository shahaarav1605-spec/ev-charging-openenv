# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port OpenEnv uses
EXPOSE 8000

# Command to start the OpenEnv server
# Replace 'env:EVChargingEnv' with 'filename:ClassName' if yours is different
CMD ["python", "-m", "openenv.server", "env:EVChargingEnv", "--host", "0.0.0.0", "--port", "8000"]