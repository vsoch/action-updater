FROM ubuntu:22.04

# docker build -t action-updater .

LABEL MAINTAINER @vsoch
ENV PATH /opt/conda/bin:${PATH}
ENV LANG C.UTF-8
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh

RUN pip install ipython
WORKDIR /code
COPY . /code
RUN pip install -e .[all]
