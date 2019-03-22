
push: build
	docker push 127.0.0.1:4999/tetris:latest

build:
	docker build -t 127.0.0.1:4999/tetris:latest .

deploy:
	-kubectl create -f ./tetris.yml
	-kubectl create -f ./cpu-test.yaml

clean:
	-kubectl delete -f ./tetris.yml
	-kubectl delete -f ./cpu-test.yaml
