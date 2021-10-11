FROM docker.io/library/python:3.8.12-alpine

WORKDIR /opt/app

COPY main.py requirements.txt /opt/app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]