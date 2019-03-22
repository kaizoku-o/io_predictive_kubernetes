FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip \
	python3-dev \
	libssl-dev \
	libffi-dev

RUN pip3 install pandas
RUN pip3 install statsmodels
RUN pip3 install sklearn
RUN pip3 install flask

ADD ./src /usr/bin/
ADD ./data /usr/bin/

WORKDIR /usr/bin/src/

ENTRYPOINT ["python3", "./main.py"]