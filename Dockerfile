FROM irid/py3

WORKDIR /
COPY ./ddns /ddns
WORKDIR /ddns
RUN pip install -r requirements.txt
CMD python ddns.py
