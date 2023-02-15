all: clean build play
build: build_net
play: play_v2ray
clean:

build_net:
	docker network create -d bridge openai || exit 0
build_restful:
	docker build -f docker/restful/Dockerfile -t aiserver . || exit 0
build_front:
	docker build -f docker/front/Dockerfile -t font . || exit 0

play_v2ray:
	docker run -d --network openai -p 2017:2017 -p 20170-20172:20170-20172 --restart=always --name v2raya -e V2RAYA_LOG_FILE=/tmp/v2raya.log -v /etc/v2raya:/etc/v2raya  mzz2017/v2raya
play_restful:
	docker run -d --network openai -p 5000:5000 --restart=always --name restful-1 aiserver || exit 0