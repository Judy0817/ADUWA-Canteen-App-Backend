FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install flask mysql-connector-python

EXPOSE 9090

CMD ["python", "api.py"]