import yaml
import datetime
from dateutil.parser import parse
from pytimeparse.timeparse import timeparse


def parseYaml(path):
    with open(path, 'r') as stream:
        try:
            return yaml.safe_load(stream)

        except yaml.YAMLError as exc:
            print(exc)


def downloadVideo(playlist, start, end, filename, path):
    print(f"Downloading {filename} to {path}")


config = parseYaml("config.yaml")
downloaded = parseYaml("downloaded.yaml")
now = datetime.datetime.now()
for subject in config:
    name = subject["name"]
    start = subject["start"]
    duration = timeparse(subject["duration"])
    period = datetime.timedelta(0, timeparse(subject["period"]))
    end = start + datetime.timedelta(0, duration)
    count = subject["count"]
    path = subject["path"]
    playlist = subject["playlist"]
    while start <= now and count > 0:
        if(not(name in downloaded and start in downloaded[name])):
            downloadVideo(playlist, start, end, f"{name}-{start}", path)
        start += period
        end += period
        count -= 1
