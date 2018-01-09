# -*- coding: utf-8 -*-
"""
Created on Sat Jan 06 18:48:00 2018

@author: Administrator
"""

import requests

def get_json():
    r = requests.get('https://api.github.com/events')
    print (r.status_code)
    print (r.json())
if __name__ == '__main__':
    get_json()