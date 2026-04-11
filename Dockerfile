FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir openenv pydantic
# Hugging Face Spaces requires port 7860
EXPOSE 7860
# We tell the server to run on 7860 instead of 8000
CMD ["python", "-m", "openenv.server", "env:EVChargingEnv", "--host", "0.0.0.0", "--port", "7860"]