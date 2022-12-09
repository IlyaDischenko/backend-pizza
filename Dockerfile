

FROM ubuntu:14.04
# MAINTAINER Prakhar Srivastav <prakhar@prakhar.me>


RUN apt-get -yqq update
# RUN apt-get install python3
RUN apt-get install python3-pip python3-dev

ADD app /opt/app
WORKDIR /opt/app

# RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

# start app
CMD [ "python", "uvicorn", "main:app", "--reload" ]