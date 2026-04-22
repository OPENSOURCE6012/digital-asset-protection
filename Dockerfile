FROM python:3.11-slim

RUN apt-get update && apt-get install -y ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY digital_asset_app/ ./digital_asset_app/

ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080"]
