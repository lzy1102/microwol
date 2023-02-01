FROM python:3.8-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN set -x \
    && apk add --no-cache tzdata libpcap-dev masscan \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
COPY pcserver.py /opt
COPY requirements.txt /opt
WORKDIR /opt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
CMD ["tail", "-f", "/dev/null"]