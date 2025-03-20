FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

COPY start.sh .
RUN chmod +x start.sh

COPY . .

CMD ["./start.sh"]