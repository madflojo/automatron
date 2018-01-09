FROM ubuntu:latest
RUN apt-get update --fix-missing && \
    apt-get -y upgrade && \
    apt-get -y install \
    python-pip \
    python-dev \
    nmap \
    curl \
    libffi-dev \
    build-essential \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*
ADD requirements.txt /
RUN pip install --upgrade setuptools pip
RUN pip install -r /requirements.txt
RUN pip install honcho
ADD . /
RUN find -name "*.sh" -exec chmod 755 {} \;
CMD honcho start
