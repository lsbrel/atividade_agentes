FROM python:3.12.3-alpine3.20

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]
