FROM python:3.9.15-slim-buster

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY bot-tg-agregate/ /app/bot-tg-agregate/
WORKDIR /app/

CMD ["python", "bot-tg-agregate/run.py"]