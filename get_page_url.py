import requests
from bs4 import BeautifulSoup

def total_url():
    """
    爬取上海所有区的板块的链接
    :return:链接与区名字典
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/61.0.3163.91 Safari/537.36',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'Connection': 'keep-alive',
               'Accept-Encoding': 'gzip, deflate'}
    url_dic = dict()
    page = requests.get("http://www.dianping.com/search/category/1/10/", headers=headers)
    bs_page = BeautifulSoup(page.text, "lxml")
    for i in bs_page.find("div", id="region-nav").find_all("a"):
        url_dic[i.text] = i.get("href")
    return url_dic
