import yaml
from dateutil.parser import parse


with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
        print(config)
        for subject in config:
            start = parse(subject["start"])
            end = parse(subject["end"])
            print(start.month)
            print(end)

    except yaml.YAMLError as exc:
        print(exc)
