FROM python:3.10-slim

COPY /src /src
COPY /config /config
COPY /locust_influx /locust_influx
COPY setup.py setup.py
COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m pip install .