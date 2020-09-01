FROM python:3.8.2

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=./src/main.py

EXPOSE 8080

ADD ./src/requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app

CMD ["flask", "run", "--port=8080", "--host=0.0.0.0"]
