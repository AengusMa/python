# -*- coding: utf-8 -*-
"""
Created on Sat Jan 06 17:03:45 2018

@author: Administrator
"""
import os
import requests
from HTMLParser import HTMLParser

class MoviePaser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies=[]
        self.in_movies = False
    def handle_starttag(self,tag,attrs):
        def _attr(attrlist,attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None
        if tag == 'li' and _attr(attrs,'data-title') and _attr(attrs, 'data-category') == 'nowplaying':
            movie = {}
            movie['title'] = _attr(attrs,'data-title')
            movie['score'] = _attr(attrs,'data-score')
            movie['director'] = _attr(attrs,'data-director')
            movie['actors'] = _attr(attrs,'data-actors')
            self.movies.append(movie)
            print('%(title)s|%(score)s|%(director)s|%(actors)s' % movie)
            self.in_movies = True
        if tag == 'img' and self.in_movies:
            self.in_movies = False
            src = _attr(attrs,'src')
            movie = self.movies[len(self.movies)-1]
            movie['poster-url'] = src
            _download_post_image(movie)

def _download_post_image(movie):
    url = movie['poster-url']
    r = requests.get(url)
    dir = 'img'
    if(os.path.exists(dir)==False):
        os.mkdir(dir) 
    fname = url.split('/')[-1]
    fname = dir + '/' +fname
    #fname = movie['title']
    with open(fname,'wb') as f:
        f.write(r.content)
        movie['poster-path'] = fname
def nowplaying_movies(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    s = requests.get(url,headers=headers)
    parser = MoviePaser()
    parser.feed(s.content) 
    return parser.movies

if __name__ == '__main__':
   url = 'https://movie.douban.com/cinema/nowplaying/wuxi/'
   movies = nowplaying_movies(url)
   import json
   print('%s' % json.dumps(movies, sort_keys=True, indent=4, separators=(',', ': ')))