all: build run

build:
	docker build -t python_api . \
	-f Dockerfile

run:
	docker-compose up

clean:
	docker image prune --force
	docker builder prune --force
	docker container prune --force