
push: build
	docker tag tetris-system-tester:latest 127.0.0.1:4999/tetris-system-tester:latest
	docker push 127.0.0.1:4999/tetris-system-tester:latest

test: pull
	docker run --rm -v $(shell pwd):/data/ 172.31.15.135:5000/tetris-system-tester:latest

pull:
	docker pull 172.31.15.135:5000/tetris-system-tester:latest

run: build
	docker run --rm -v $(shell pwd):/data/ -it tetris-system-tester:latest

build:
	docker build -t tetris-system-tester:latest .
