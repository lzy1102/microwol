all: clean build play
build:
	docker network create -d bridge openpc || exit 0
	docker build -t openpc . || exit 0
play:
	#docker run -d --network openpc --name emqx-1 -p 1883:1883 -p 18083:18083 --restart=always emqx
	docker run -d --network openpc -p 5000:5000 --name openpc-1 -v /data/microserver/instance:/opt/instance --restart=always openpc || exit 0
clean:
	rm -irf /mosquitto
	docker stop openpc-1 | xargs docker rm || exit 0