all: clean build play
build: build_net
play: play_v2ray
clean:

build_net:
	docker network create -d bridge openai || exit 0
build_ai:
	docker build -t aiserver . || exit 0

play_v2ray:
	docker run -d --network openai -p 2017:2017 -p 20170-20172:20170-20172 --restart=always --name v2raya -e V2RAYA_LOG_FILE=/tmp/v2raya.log -v /etc/v2raya:/etc/v2raya  mzz2017/v2raya
play_ai:
	docker run -d --network openai -v $$PWD:/opt/server -p 5000:5000 --restart=always --name ai-1 aiserver || exit 0