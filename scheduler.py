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


def writeYaml(obj, path):
    with open(path, 'w') as file:
        yaml.dump(obj, file)


def getVideoUrl(playlist):
    text = subprocess.check_output(["youtube-dl", "--dump-json", "--flat-playlist",
                                    playlist], encoding='utf-8').partition('\n')[0]

    obj = json.loads(text)
    return f"https://youtu.be/{obj['id']}"


def downloadVideo(playlist, start, end, filename, path):
    print(f"Downloading {filename} into {path}")
    url = getVideoUrl(playlist)
    dateformat = "%-d.%-m.%Y %H:%M"
    filepath = os.path.join(path, filename) + ".mp4"
    startStr = start.strftime(dateformat)
    endStr = end.strftime(dateformat)
    process = subprocess.run(
        ["yt_ddl","-vf","1", "-s", startStr, "-e", endStr, url, "-o", filepath])
    return process.returncode


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

    if not os.path.exists(path):
        print(f"Path {path} does not exist. Creating it now...")
        os.mkdir(path)
    while end <= now and count > 0:
        if(not(name in downloaded and start in downloaded[name])):
            res = downloadVideo(playlist, start, end,
                                f"{name}_{start.strftime('%-d.%-m.%Y_%H%M')}", path)
            if res == 0:
                print("Download was succesful.")
                if name not in downloaded:
                    downloaded[name] = [start]
                else:
                    downloaded[name].append(start)
                writeYaml(downloaded, "downloaded.yaml")
            else:
                print("There was an error.")
        start += period
        end += period
        count -= 1
