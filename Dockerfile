FROM python:3.10-slim-buster

WORKDIR /mechanic

RUN apt-get update -yqq \
    && apt-get install -yqq \
    libhidapi-hidraw0 \
    python3-pigpio \
    python3-gpiozero

RUN python3 -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY mechanic ./mechanic/
COPY setup.py ./
COPY config.json ./

RUN pip install .

EXPOSE 7070

ENTRYPOINT [ "mechanic" ]
