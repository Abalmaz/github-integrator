FROM python:3.8.2

RUN mkdir /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app

#WORKDIR /app
#RUN pip install --upgrade pip setuptools
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
#EXPOSE 5000
#COPY . /app

CMD ["flask", "run"]