FROM python:3.8.2

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ../src/requirements.txt /app/
RUN pip install -r requirements.txt

ADD .. /app

CMD ["flask", "run"]
