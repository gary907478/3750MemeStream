FROM python:3.4-slim-jessie

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    mariadb-client \
    python-mysqldb \
    python3-dev \
    libmysqlclient-dev \
    build-essential \
    iputils-ping && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir memeStream

RUN pip install --no-cache-dir --trusted-host curl mysqlclient requests Flask

COPY . memeStream

WORKDIR memeStream

RUN ./build.sh

EXPOSE 8080

CMD ["./run.sh"]
