FROM httpd:2.4
RUN set -ex; \
    apt update; apt install -y --no-install-recommends \
    wget \
    unzip
WORKDIR /usr/local/apache2/htdocs
RUN wget --no-check-certificate https://github.com/ETS-Smart-House/SmartHouseClient/archive/refs/heads/main.zip
RUN unzip main.zip
RUN cp -R ./SmartHouseClient-main/* ./
