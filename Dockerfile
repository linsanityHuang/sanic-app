FROM python:3.7.4
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    git \
    supervisor \
	nginx \
    net-tools \
    vim \
    sqlite3 && \
   rm -rf /var/lib/apt/lists/*

COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisor/supervisor-app.conf /etc/supervisor/conf.d/

RUN mkdir /app

# 设置工作目录
WORKDIR /app

# 将目录alm-report加入到工作目录中
ADD app /app
RUN pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com --upgrade pip
RUN pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -r requirements.txt

# 设置环境变量
ENV TZ=Asia/Shanghai
ENV config_url=http://52.82.117.255:8081/calculate

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/nginx-app.conf /etc/nginx/sites-available/

# 对外暴露端口
EXPOSE 1338 9001

CMD ["supervisord", "-n"]
