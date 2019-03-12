FROM ubuntu:18.04
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install stress-ng -y
ADD mem-run.sh /usr/bin/
RUN chmod +x /usr/bin/mem-run.sh
ENTRYPOINT []
