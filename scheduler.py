import yaml
import datetime
from dateutil.parser import parse
from pytimeparse.timeparse import timeparse


with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)

    except yaml.YAMLError as exc:
        print(exc)

with open("downloaded.yaml", 'r') as stream:
    try:
        downloaded = yaml.safe_load(stream)

    except yaml.YAMLError as exc:
        print(exc)

now = datetime.datetime.now()
for subject in config:
    name = subject["name"]
    start = subject["start"]
    duration = timeparse(subject["duration"])
    period = datetime.timedelta(0, timeparse(subject["period"]))
    end = start + datetime.timedelta(0, duration)
    count = subject["count"]
    path = subject["path"]

    while start <= now and count > 0:
        if(not(name in downloaded and start in downloaded[name])):
            print(f"Downloading {name} {start} to {path}")
        start += period
        end += period
        count -= 1
