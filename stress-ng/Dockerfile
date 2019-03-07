FROM ubuntu:18.04
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install stress-ng -y
ENTRYPOINT ["/usr/bin/stress-ng"]
CMD ["--help"]
