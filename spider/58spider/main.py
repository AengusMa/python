from multiprocessing import Pool
from channel_extact import channel_list
from pages_parsing import get_links_from
import pymongo

con = pymongo.MongoClient('localhost', 27017)
table = con.test.spider_urls


def get_all_links_from(channel):
    for i in range(1, 100):
        urls = get_links_from(channel, i)
        table.insert(urls)


if __name__ == '__main__':
    # table.remove()
    pool = Pool(processes=8)
    pool.map(get_all_links_from, channel_list.split())
