FROM python:3.9.3

COPY bots/config.py /bots/
COPY bots/journalists.txt /bots/
COPY bots/good_accounts.txt /bots/
COPY bots/NapoliNewsBot.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "NapoliNewsBot.py"]