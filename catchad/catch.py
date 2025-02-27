import requests  # 发送请求
import pandas as pd  # 存入csv数据
import time  # 等待间隔
import random  # 随机
import re  # 用正则表达式提取url
import traceback
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)

with open('citys.txt', encoding='utf-8') as file:
    citys = file.readlines()
with open('needs.txt', encoding='utf-8') as file:
    needs = file.readlines()

# 伪装浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Host": "www.baidu.com",
    # 需要更换Cookie
    "Cookie": 'you_cookie'
}


def baidu_search(v_keyword, v_max_page):
    """
    爬取百度搜素结果
    :param v_max_page: 爬取前几页
    :param v_keyword: 搜索关键词
    :param v_result_file: 保存文件名
    :return: None
    """
    # 获得每页搜索结果
    for page in range(v_max_page):
        print('开始爬取第{}页'.format(page + 1))
        wait_seconds = random.uniform(1, 2)  # 等待时长秒
        print('开始等待{}秒'.format(wait_seconds))
        time.sleep(wait_seconds)  # 随机等待
        url = 'https://www.baidu.com/s?wd=' + \
              v_keyword + '&pn=' + str(page * 10)
        r = requests.get(url, headers=headers)
        html = r.text
        link = re.findall(
            "https://ada.baidu.com/site/.*?xyl.imid........................................", html)
        url = []
        site = []
        for i in link:
            j = i.split('/')[4]
            k = i.split('/')[5]
            if k.startswith('xyl'):
                url.append(i)
                site.append(j)
        result = {"url": url, "site": site}
        data = pd.DataFrame(result)
        data = data.drop_duplicates(['site'])
        data = data.set_index(['url'])
        print(1)
        print(data)
        data.to_csv('baidu_ad_site.csv', mode='a', header=None)
        print('保存成功')
        print('\n\n\n')


def baidu_deep_search(url, keywords):
    """
    尝试深度爬取页面内容，一些网页中不能直接获取营销组件链接，但有相关关键字可以利用
    :param url: 爬取网址
    :param keywords: 搜索关键字，如“在线咨询”，“联系我们”等
    """
    # 搜索是否出现“咨询”这个词语



if __name__ == '__main__':
    count = 0
    for city in citys:
        for need in needs:
            if count == 10:
                break
            count += 1

            try:
                search_keyword = f"{city.strip()}+{need}"
                print(search_keyword)
                baidu_search(v_keyword=search_keyword, v_max_page=1)
            except Exception:
                traceback.print_exc()
                time.sleep(60)
                pass
