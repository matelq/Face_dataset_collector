import sys
import os
import ffmpeg
from pytube import YouTube


def downloader():

    os.makedirs('downloads', exist_ok=True)

    class UrlInfo:
        def __init__(self, url, key):
            self.url = url
            self.key = key

    with open('urls_from_keys.csv', 'r') as f:
        lines = f.readlines()
        lines = [x.split(',') for x in lines]
        url_infos = [UrlInfo(x[0], x[1]) for x in lines]

    for ui in url_infos:
        yt = YouTube(ui.url)
        yt.streams.get_by_resolution('360p').download('./downloads')



