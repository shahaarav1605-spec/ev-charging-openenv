FROM python:3.10-slim

WORKDIR /app

# Copy all files from your VS Code folder
COPY . .

# Install dependencies
RUN pip install --no-cache-dir pydantic==2.6.1 openenv

# Set PYTHONPATH so Python can see your files
ENV PYTHONPATH=/app

# Standard Port for Hugging Face
EXPOSE 7860

# CMD [ "filename" : "ClassName" ]
CMD ["python", "-m", "openenv.server", "env:EVChargingEnv", "--host", "0.0.0.0", "--port", "7860"]