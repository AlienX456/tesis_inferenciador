FROM ubuntu:bionic

RUN apt update &&\
    apt install -y software-properties-common &&\
    apt install -y python3-pip &&\
    pip3 install https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-linux_x86_64.whl &&\
    pip3 install https://download.pytorch.org/whl/cpu/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl &&\
    pip3 install flask-restful


COPY requirements.txt /inferenciador/
COPY adapa/dcase_adapatask5.py /inferenciador/adapa/
COPY api/api.py /inferenciador/api/
COPY interfaz/__init__.py interfaz/inferenciador.py /inferenciador/interfaz/
COPY data/*  /inferenciador/data/

RUN pip3 install -r /inferenciador/requirements.txt


EXPOSE 5000

