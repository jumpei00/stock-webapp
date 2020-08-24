FROM python:3.8

RUN apt-get update && apt-get install -y wget
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install

WORKDIR /usr/src/stockapp
COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt