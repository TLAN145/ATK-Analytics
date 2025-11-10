# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY custom_exporter.py .
RUN pip install prometheus_client requests
EXPOSE 9200
CMD ["python", "custom_exporter.py"]
