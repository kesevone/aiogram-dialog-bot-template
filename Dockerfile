FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

COPY . .
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]