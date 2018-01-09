# -*- coding: utf-8 -*-
"""
Created on Sat Jan 06 17:03:45 2018

@author: Administrator
"""
import urllib2
from HTMLParser import HTMLParser

class MoviePaser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies=[]
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
            

def nowplaying_movies(url):
    headers = {}
    req = urllib2.Request(url,headers=headers)
    s = urllib2.urlopen(req)
    parser = MoviePaser()
    parser.feed(s.read())
    s.close()
    return parser.movies

if __name__ == '__main__':
   url = 'https://movie.douban.com/cinema/nowplaying/wuxi/'
   movies = nowplaying_movies(url)
   import json
   print('%s' % json.dumps(movies, sort_keys=True, indent=4, separators=(',', ': ')))