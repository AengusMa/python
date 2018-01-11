# -*- coding: utf-8 -*-
import requests
import os
import threading

gImageList = []
gCondition = threading.Condition()

class Consumer(threading.Thread):
    def __init__(self, folder='wallpaper', group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Consumer, self).__init__(group, target, name, args, kwargs, verbose)
        self.folder = folder
    def run(self):
        global gImageList
        global gCondition
        print ('%s started' % threading.current_thread())
        while True:
            gCondition.acquire()
            print('%s:trying to download image.Queue length is %d ' % (threading.current_thread(),len(gImageList)))
            while len(gImageList) == 0:
                gCondition.wait()
                print('%s:wake up.Queue length is %d' % (threading.current_thread(),len(gImageList)))
            url = gImageList.pop()
            gCondition.release()

            _download_image(url,self.folder)
class Producer(threading.Thread):
    def run(self):
        global gImageList
        global gCondition

        print ('%s started' % threading.current_thread)
        imgs = download_wallpape_list()

        gCondition.acquire()
        for img in imgs:
            if 'downloadUrl' in img:
                gImageList.append(img['downloadUrl'])
        print('%s: produced %d urls. Left %d urls.' % (threading.current_thread(), len(imgs) - 1, len(gImageList)))
        gCondition.notify_all()
        gCondition.release()


def _download_image(url,folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    print('%s:downloading %s' % (threading.current_thread(),url))
    filename= lambda s:os.path.join(folder,os.path.split(url)[1])
    r = requests.get(url)
    with open(filename(url),'wb') as f :
        f.write(r.content)
    return filename(url)
def download_wallpape_list():
    #http://image.baidu.com/channel/wallpaper#%E5%8A%A8%E6%BC%AB&%E5%85%A8%E9%83%A8&8&0
    url = 'http://image.baidu.com/data/imgs'
    params ={
        'pn':0,
        'rn':100,
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
    #for i in imgs:
     #   if 'downloadUrl' in i:
      #      _download_image(i['downloadUrl'],'wallpaper')
    return imgs
if __name__ =='__main__':
    Producer().start()
    for i in range(3):
        Consumer().start()