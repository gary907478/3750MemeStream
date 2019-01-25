FROM mysql:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    iputils-ping && \
    mkdir memeStream && \
    rm -rf /var/lib/apt/lists/*

ENV MYSQL_ROOT_PASSWORD="notwaterloo"
ENV MYSQL_DATABASE="memestreamdb"

COPY . memeStream

WORKDIR memeStream

EXPOSE 3306

RUN cp db.sql /docker-entrypoint-initdb.d/
