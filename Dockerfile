FROM python:3.12-slim

WORKDIR /opt/app
ENV PYTHONPATH=/opt/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY data/ ./data/
COPY src/ ./src

ENTRYPOINT ["python", "src/main.py"]
