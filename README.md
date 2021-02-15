# Youtube Stream Download Scheduler - YSDS

With YSDS you can periodically download parts of a running youtube stream.

## Usage
This will start downloading pending downloads if there are any. It is best to run this periodically using for example `systemd`.
```bash
python ./scheduler.py
```
## Instalation
Download and unpack this repository. Then install dependencies with `pip install -r requirements.txt`

## Configuration
Use the `config.yaml` file to define your downloads.

```yaml

- name: IDS                                                                             #name of the section
  path: /mnt/d/jiriv/Documents/IDS                                                      #path to folder where streams should be downloaded
  playlist: https://www.youtube.com/playlist?list=PL_eb8wrKJwYuNXjVXtm_Tyh9mf5gT9Xrr    #url of the youtube playlist
  start: 2021-02-09 10:00:00                                                            #timestamp with the start of the part of the stream you want to download
  duration: 3h                                                                          #duration of the part of the stream
  period: 168h                                                                          #period (after how much time should another part be downloaded)
  count: 13                                                                             #how many parts do you want to download

```
## The `downloaded.yaml` file

Parts that were downloaded are stored in the `downloaded.yaml` file so they are not downloaded again. You can manually edit it if you don't want a part to be downloaded sometime.
```yaml
IDS:
  - 2021-02-09 10:00:00
```
