FROM ubuntu:14.04
RUN apt-get update --fix-missing && \
    apt-get -y upgrade && \
    apt-get -y install \
    python-pip \
    python-dev \
    nmap
ADD requirements.txt /
RUN pip install --upgrade setuptools
RUN pip install -r /requirements.txt
RUN pip install honcho
ADD . /
RUN find -name "*.sh" -exec chmod 755 {} \;
CMD honcho start
