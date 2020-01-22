FROM ubuntu:latest

ADD . /pa
WORKDIR /pa

RUN apt-get -y update
RUN apt-get -y install libpq-dev python3 python3-pip
RUN pip3 install -r requirements.txt
RUN export LC_ALL=en_US.utf-8 && export LANG=en_US.utf-8


EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
