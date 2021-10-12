all: build run

build:
	docker build -t python_api \
	-f Dockerfile \
	.

run:
	docker-compose up

clean:
	rm -rf __pycache__/
	docker image prune --force
	docker builder prune --force
	docker container prune --force