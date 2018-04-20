# manaba-attend

[Manaba の出席カード](https://atmnb.tsukuba.ac.jp/attend/tsukuba)の提出を自動化するプログラム。

Program automating to send your attendance on Manaba.

[<img alt="Demo video" width="400" src="https://j.gifs.com/Xo5Y38.gif">](https://youtu.be/9ZQMev_WQeE)

## Requirement

- Python3
- Google Chrome
- HomeBrew

## Installation

```shell
$ brew install chromedriver
$ pip install -r requirements.txt
```

## Usage

```shell
$ python main.py -h
usage: main.py [-h] [--no-headless] attend_code

positional arguments:
  attend_code

optional arguments:
  -h, --help     show this help message and exit
  --no-headless  specify to open the browser window.
```

## Note

If you want to specify your ID & password via the environment variable, please set them into `MANABA_USERNAME` & `MANABA_PASSWORD`.