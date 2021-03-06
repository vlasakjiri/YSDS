import yaml
import datetime
from dateutil.parser import parse
from pytimeparse.timeparse import timeparse
import subprocess
import json
import os


def parseYaml(path):
    with open(path, 'r') as stream:
        try:
            obj = yaml.safe_load(stream)
            if obj is None:
                obj = dict()
            return obj

        except yaml.YAMLError as exc:
            print(exc)


def getVideoUrl(playlist):
    text = subprocess.check_output(["youtube-dl", "--dump-json", "--flat-playlist",
                                    playlist], encoding='utf-8').partition('\n')[0]

    obj = json.loads(text)
    return f"https://youtu.be/{obj['id']}"


def downloadVideo(playlist, start, end, filename, path):
    url = getVideoUrl(playlist)
    dateformat = "%-d.%-m.%Y %H:%M"
    filepath = os.path.join(path, filename)
    startStr = start.strftime(dateformat)
    endStr = end.strftime(dateformat)
    process = subprocess.run(
        ["yt_ddl", "-vf", "1", "-s", startStr, "-e", endStr, url, "-o", filepath])
    return process.returncode


config = parseYaml("config.yaml")
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
    no_older_than = datetime.timedelta(
        0, timeparse(subject.get("no_older_than"))) if "no_older_than" in subject else None

    if not os.path.exists(path):
        print(f"Path {path} does not exist. Creating it now...")
        os.mkdir(path)
    while end <= now and count > 0:
        filename = f"{name}_{start.strftime('%-d.%-m.%Y_%H%M')}.mp4"
        downloaded = os.listdir(path)
        if(not(filename in downloaded) and (no_older_than is None or now - start <= no_older_than)):
            print(f"Downloading {filename} into {path}")
            res = downloadVideo(playlist, start, end,
                                filename, path)
            if res == 0:
                print("Download was succesful.")
            else:
                print("There was an error.")
        start += period
        end += period
        count -= 1
