FROM python

WORKDIR /usr/src/app

COPY ApiCalls.py .

COPY client.py .

COPY script.sh .

RUN pip install mechanize

RUN pip install requests

RUN mkdir ./data

RUN mkdir ./data/credentials

RUN mkdir ./data/logs

CMD ["./script.sh", "2"]