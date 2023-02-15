FROM ubuntu
ENV LANG C.UTF-8
ENV TZ Asia/Shanghai
ARG DEBIAN_FRONTEND=noninteractive
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
RUN apt clean && apt -y update && apt install tzdata python3 python3-pip unzip wget curl xvfb ffmpeg -y

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN set -x \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && pip install -U pip \
    && pip install -U setuptools \
    && mkdir -p /opt/server

COPY . /opt/server/

RUN mv /opt/server/chromedriver /usr/bin/
RUN chmod +x /usr/bin/chromedriver
RUN apt install -y /opt/server/google-chrome-stable_current_amd64.deb

WORKDIR /opt/server

RUN pip install -r requirements.txt
RUN ffdl install -y

ENTRYPOINT ["python3","main.py"]