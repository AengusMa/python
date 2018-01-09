# -*- coding: utf-8 -*-
"""
Created on Sat Jan 06 13:38:03 2018

@author: Administrator
"""
import urllib

def print_list(l):
    for i in l:
        print (i);
def demo():
    s = urllib.urlopen('http://blog.kamidox.com')
    msg = s.info()
    print_list(dir(msg) )
def process(block,block_size,totle_size):
    print ('%d/%d - %.02f%%' % (block*block_size,totle_size,(float)(block*block_size)*100/totle_size))
def retrieve():
    s = urllib.urlretrieve('http://blog.kamidox.com','index.html',reporthook=process)
    
if __name__ == '__main__':
    retrieve()