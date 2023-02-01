all: clean build play
build:
	docker build -t openpc .
play:
	docker run -d -p 5000:5000 --name openpc-1 openpc
clean:
	docker stop openpc-1 | xargs docker rm || exit 0