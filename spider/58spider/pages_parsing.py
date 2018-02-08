from bs4 import BeautifulSoup
import requests
import time


def get_links_from(channel, pages, who_sells=0):
    time.sleep(1)
    urls = []
    list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
    wd_data = requests.get(list_view)
    soup = BeautifulSoup(wd_data.text, 'lxml')
    if who_sells == 0:
        links = soup.select('td.t a.t')
    else:
        links = soup.select('.commonInfo a.business_img')
    for link in links:
        url = link.get('href').split('?')[0]

        # print(link.get('href').split('?')[0])
        tmp = {'url': url}
        urls.append(tmp)
        print(url)
    return urls


def get_views_from(url):
    id = url.split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    js = requests.get(api)
    views = js.text.split('=')[-1]
    return views


def get_item_info(url):
    if url.startswith('http://bj.58.com'):
        who_sells = 1
    else:
        who_sells = 0
    wd_data = requests.get(url)
    soup = BeautifulSoup(wd_data.text, 'lxml')
    # no_longer_exist='404' in soup.find('script',type='text/javascript').get('src').spilt('/')
    no_longer_exist = len(soup.select('.content .head .et'))
    if no_longer_exist:
        return
    if who_sells == 0:
        data = {
            'title': soup.title.text,
            'price': soup.select('.price_now')[0].text,
            'area': soup.select('.palce_li i')[0].text,
            'cate': '个人' if who_sells == 0 else '商家',
            'views': soup.select('.look_time')[0].text[:-3],
            'wanted': soup.select('.want_person')[0].text[:-3],
            'url': url,
        }
    else:
        data = {
            'title': soup.title.text,
            'price': soup.select('.price')[0].text,
            'area': list(soup.select('.c_25d')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None,
            'date': soup.select('.time')[0].text,
            'cate': '个人' if who_sells == 0 else '商家',
            'views': get_views_from(url),
            'url': url,
        }
    return data


url_list = get_links_from('http://bj.58.com/shouji/', 0, 1)
# http://bj.58.com/shouji/33021870150069x.shtml
# http://zhuanzhuan.58.com/detail/960855608383635463z.shtml
# get_item_info('http://zhuanzhuan.58.com/detail/9608556083836353z.shtml', 0)
