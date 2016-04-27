FROM python:2.7

RUN apt-get update && apt-get install -y software-properties-common python-software-properties && apt-get update

RUN apt-get install -y python cron




#ADD src /work
ADD src/requirements.txt /work/requirements.txt
RUN pip install -r /work/requirements.txt

ADD run.sh /run.sh
RUN chmod 744 /run.sh
WORKDIR /work

CMD ["/run.sh"]
