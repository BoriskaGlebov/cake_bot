FROM python:3.12.0-slim

COPY requirements.txt /bot/

RUN pip install -r /bot/requirements.txt

COPY . /bot/

WORKDIR /bot

ENTRYPOINT ["python3","main.py"]
