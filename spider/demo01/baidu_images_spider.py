# -*- coding: utf-8 -*-
import requests
import os

def _download_image(url,folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    print('downloading %s' % url)
    filename= lambda s:os.path.join(folder,os.path.split(url)[1])
    response = requests.get(url)
    with open(filename(url), 'wb') as fd:
        for chunk in response.iter_content(128):
            fd.write(chunk)
    return filename(url)
def download_wallpaper():
    #http://image.baidu.com/channel/wallpaper#%E5%8A%A8%E6%BC%AB&%E5%85%A8%E9%83%A8&8&0
    url = 'http://image.baidu.com/data/imgs'
    params ={
        'pn':25,
        'rn':35,
        'col':'壁纸',
        'tag':'动漫',
        'tags':'全部',
        'width':1366,
        'height':768,
        'ic':0,
        'ie':'utf-8',
        'oe':'utf-8',
        'image_id':'',
        'fr':'channel',
        'p':'channel',
        'from':1,
        'app':'img.browse.channel.wallpaper',
        't':'0.618244607346601'
    }
    s = requests.get(url,params=params)
    imgs = s.json()['imgs']
    print ('totally %d images to downlaod'%len(imgs))
    for i in imgs:
        if 'downloadUrl' in i:
            _download_image(i['downloadUrl'],'wallpaper')
if __name__ =='__main__':
    download_wallpaper()