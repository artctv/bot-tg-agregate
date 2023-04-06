FROM python:3.9.15-slim-buster

COPY bot-tg-agregate/ app/bot-tg-agregate
COPY requirements.txt /app/

WORKDIR /app/

RUN pip install -r requirements.txt

CMD ["python", "bot-tg-agregate/run.py"]