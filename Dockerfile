FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app/src

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]