# -*- coding: utf-8 -*-

import requests
from HTMLParser import HTMLParser

class DoubanClient(object):
    def __init__(self):
        object.__init__(self)
        headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
                   'origin': 'http://www.douban.com'} 
        self.session = requests.session()
        self.session.headers.update(headers)
    def login(self,username,password,
              source='index_nav',
              redir='http://www.douban.com/',
              login='登录'):
        #access login page to get captcha
        url = 'https://www.douban.com/accounts/login'
        r = self.session.get(url)
        (captcha_id,captcha_url) = _get_captcha(r.content)
        if captcha_id:
            captcha_solution = raw_input('please input solution for captcha[%s]:'%captcha_url)
           # captcha_solution = raw_input('please input solution for captcha[%s]:'',captcha_url)
        #post login request
        data = {'form_email':username,
                'form_password':password,
                'source':source,
                'redir':redir,
                'login':login}
        if captcha_id:
            data['captcha-id'] = captcha_id
            data['captcha-solution'] = captcha_solution
        headers = {'referer':'http://www.douban.com/accounts/login?source=main',
                   'host':'accounts.douban.com'}
        r = self.session.post(url,data=data,headers = headers)
        print (self.session.cookies.items())
        pass
    def edit_signature(self,username,signature):
        #access user's homepage
        #url1 = 'https://www.douban.com/people/172159744/'
        url1 = 'https://www.douban.com/people/'+username+'/'
        r = self.session.get(url1)
        ck = _get_ck(r.content)
        #post reqeust to chang signature
        #url = 'https://www.douban.com/j/people/172159744/edit_signature'
        url = 'https://www.douban.com/j/people/'+username+'/edit_signature'
        headers = {'referer':'https://www.douban.com/people/172159744/',
                   'host':'www.douban.com',
                   'x-requested-with':'XMLHttpRequest'}
        data = {'ck':ck,'signature':signature}
        r = self.session.post(url,data=data,headers=headers)
        print (r.content)
    
def _attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None

def _get_captcha(content):
    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_id = None
            self.captcha_url = None
        def handle_starttag(self,tag,attrs):
           
           # if tag == 'input' and _attr(attrs,'type')=='hidden'and _attr(attrs,'name')=='captcha_id':
            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'captcha-id':
                self.captcha_id = _attr(attrs,'value')
                print ('='*10)
            if tag == 'img' and _attr(attrs,'id')=='captcha_image' and _attr(attrs,'class')=='captcha_image' :
                self.captcha_url = _attr(attrs,'src')
            pass
    p = CaptchaParser()
    p.feed(content)
    return p.captcha_id,p.captcha_url
def _get_ck(content):
    class CKParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck = None
        def handle_starttag(self,tag,attrs):
            if tag == 'input' and _attr(attrs,'type')=='hidden' and _attr(attrs,'name')=='ck':
                self.ck = _attr(attrs,'value')
    p = CKParser()
    p.feed(content)
    return p.ck
if __name__ == '__main__':
    c = DoubanClient()
    c.login('mwljndx@163.com','m89676378')
    c.edit_signature('172159744','edit')
    