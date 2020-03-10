# name:extractor-af
FROM python:3

ADD extract.py /
ADD config.json /

RUN pip install boto3 requests

CMD [ "python", "./extract.py" ]