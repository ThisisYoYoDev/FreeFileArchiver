FROM python:3.11.4-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

COPY . .

CMD ["python", "main.py"]