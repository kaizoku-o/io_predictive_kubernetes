FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
	john \
	vim

COPY password-to-crack.txt /tmp/password-to-crack.txt

ENTRYPOINT ["/usr/sbin/john", "/tmp/password-to-crack.txt"]
