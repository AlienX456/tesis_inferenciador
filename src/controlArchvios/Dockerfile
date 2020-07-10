from ubuntu:bionic

COPY interfaz/* /control/interfaz/
COPY src/* /control/src/
COPY test /control/test/
COPY requirements.txt /control/

RUN apt update &&\
    apt -y install software-properties-common &&\
    add-apt-repository -y ppa:deadsnakes/ppa &&\
    apt -y install python3.7 &&\
    apt -y install python3-pip


WORKDIR /control/


RUN python3.7 -m pip install -r requirements.txt