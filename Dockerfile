FROM python:3.7-slim

COPY . /app
COPY requirements.txt /app

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "mincecraftbot.py"]
