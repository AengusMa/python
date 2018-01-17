# -*- coding: utf-8 -*-
# @Author: mwl
# 必应图片下载,文件名为当天日期
import os
import requests
from HTMLParser import HTMLParser
import re
import time


def _download_image(url,folder='img'):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    print('downloading %s' % url)
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    filename= lambda s:os.path.join(folder,date+".jpg")
    response = requests.get(url)
    with open(filename(url), 'wb') as fd:
        for chunk in response.iter_content(128):
            fd.write(chunk)
    return filename(url)
def getPicturesUrl():
    url = 'https://cn.bing.com'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    s = requests.get(url,headers=headers)
    #));;g_img={url: "/az/hprichbg/rb/BarHarborCave_ZH-CN8055769470_1920x1080.jpg",id
    m = re.search(r'g_img=\{url: "(.+?)",',s.content,re.S)
    purl ='https://cn.bing.com'+m.group(1)
    _download_image(purl)

if __name__ == '__main__':
    getPicturesUrl()
