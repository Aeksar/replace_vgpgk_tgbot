FROM python:3.13-slim

WORKDIR /replace_bot

RUN apt-get update && apt-get install -y libreoffice

COPY requirements.txt .
RUN pip install --no-cache-di -r requirements.txt

COPY . .

RUN ["python3", "main.py"]
