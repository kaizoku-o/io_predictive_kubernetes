

all: build
	docker run --rm -v $(shell pwd):/data/ -it tetris-system-tester:latest

build:
	docker build -t tetris-system-tester:latest .
