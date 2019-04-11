 diffFROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip \
	python3-dev \
	libssl-dev \
	libffi-dev \
	vim \
	cron \
	curl

RUN pip3 install pandas
RUN pip3 install statsmodels
RUN pip3 install sklearn
RUN pip3 install flask
RUN pip3 install requests

ADD src /usr/bin/src/

RUN chmod +x /usr/bin/src/precompute_scheduler.sh
RUN chmod +x /usr/bin/src/install_cron_entry.sh

ADD data/ /usr/bin/data

WORKDIR /usr/bin/src/
RUN /bin/bash -c "source /usr/bin/src/install_cron_entry.sh"
ENTRYPOINT ["python3", "./main.py"]
