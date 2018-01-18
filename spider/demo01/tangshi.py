# _*_ coding:utf-8 _*_

from HTMLParser import HTMLParser
import requests
import re


def _attr(attrs,attrname):
    for attr in attrs:
        if(attr[0]) == attrname:
            return attr[1]
    return None
class PoemParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tangshi_list = []
        self.in_div = False
        self.in_a = False
        self.in_span = False
        self.poems = {}
        self.pattern = re.compile(r'\((.*)\)')
        #g_img={url: "/az/hprichbg/rb/BarHarborCave_ZH-CN8055769470_1920x1080.jpg"
    def handle_starttag(self,tag,attrs):
        if tag == 'div' and _attr(attrs,'class')=='typecont':
            self.in_div = True
        if tag == 'span':
            self.in_span = True
        if self.in_span and tag == 'a':
            self.in_a  =True
            self.poems['url'] = _attr(attrs,'href')
    def handle_endtag(self,tag):
        if tag == 'div':
            self.in_div = False
        if tag == 'a':
            self.in_a = False
        if tag == 'span':
            self.in_span = False
    def handle_data(self,data):
        if self.in_span:
            print (data)
           
            m = self.pattern.match(data)
            if m:
                self.poems['author'] = m.group(1)
                self.tangshi_list.append(self.poems)
                self.poems = {}
            else:
                self.poems['title'] = data


def retrive_tangshi_300():
    url = 'http://www.gushiwen.org/gushi/tangshi.aspx'
    r = requests.get(url)
    p =PoemParser()
    p.feed(r.content)
    return p.tangshi_list


if __name__ =='__main__':
    l = retrive_tangshi_300()
    for i in range(len(l)):
        print ('标题:%(title)s\t作者:%(author)s\tURL:%(url)s')%(l[i])
    print('total %d poems.'%len(l))