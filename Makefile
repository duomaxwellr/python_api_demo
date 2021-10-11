all: build run

build:
	docker build -t python_api . \
	-f Dockerfile

run:
	docker-compose up