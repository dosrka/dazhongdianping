import datetime
import random
import time
import traceback

import requests
from bs4 import BeautifulSoup
from mysql_unit import insert_sql

from yu.get_page_url import total_url


def req_pages(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/61.0.3163.91 Safari/537.36',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'Connection': 'keep-alive',
               'Accept-Encoding': 'gzip, deflate'}

    try:
        page = requests.get(url, headers=headers)
    except:
        page = None
        print("无法请求页面: " + url)
    finally:
        return page.text


def bs4_pages(page):
    content_dic = dict()
    bs0bj = BeautifulSoup(page, 'lxml')
    for li in bs0bj.find_all("div", class_="txt"):
        # 店名
        dic_key_name = li.find("div", class_="tit").find("a", onclick=True).get("title")
        # 店铺星级
        dic_value_star = li.find("span", class_=True).get("title")
        # 店铺点评数
        try:
            dic_value_remark = li.find("a", onclick='LXAnalytics(\'moduleClick\', \'shopreview\')').find("b").text
        except:
            print("此项没有点评人数信息。")
            dic_value_remark = "None"
        # 店铺人均消费
        try:
            dic_value_expend = li.find("a", onclick='LXAnalytics(\'moduleClick\', \'shopprice\')').find("b").text
        except:
            print("此项没有人均消费信息。")
            dic_value_expend = "None"
        # 店铺菜系
        dic_value_style = li.find("div", class_="tag-addr").find_all("span", class_="tag")[0].text
        # 店铺位置
        dic_value_addr = li.find("div", class_="tag-addr").find_all("span", class_="tag")[1].text
        # 添加到列表中
        dic_value = [dic_value_star, dic_value_style, dic_value_expend, dic_value_remark, dic_value_addr]
        content_dic[dic_key_name] = dic_value
        print(1)
    print(2)
    return content_dic


def page_content(url):
    random.seed(datetime.datetime.now())
    page_num = 1
    while page_num <= 50:
        print("正在打印第%s页" % page_num)
        page = req_pages(url+"p"+str(page_num))
        try:
            content = bs4_pages(page)
        except Exception as e:
            print(traceback.format_exc())
        try:
            insert_sql(content)
        except Exception as e:
            print("插入失败，第"+str(page_num)+"页")
        page_num += 1
        sleep_time = random.randint(2, 5)
        print("等待"+str(sleep_time)+"秒")
        time.sleep(sleep_time)


def task_spider():
    total_name_url = total_url()
    region = 1
    for key, value in total_name_url.items():
        print(key, value)
        print("正在打印第" + str(region) + "个区域" + str(key))
        page_content(value)
        region += 1


if __name__ == "__main__":
    task_spider()
