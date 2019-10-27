FROM python:3.6

ADD . /pa
WORKDIR /pa

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]