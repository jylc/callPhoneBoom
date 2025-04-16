import requests  # 发送请求
import pandas as pd  # 存入csv数据
import time  # 等待间隔
import random  # 随机
import re  # 用正则表达式提取url
import traceback
from urllib.parse import quote
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)

with open('citys.txt', encoding='utf-8') as file:
    citys = file.readlines()
with open('needs.txt', encoding='utf-8') as file:
    needs = file.readlines()

# 伪装浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Host": "www.baidu.com",
    # 需要更换Cookie
    "Cookie": 'sug=3; sugstore=0; ORIGIN=2; bdime=0; BD_UPN=12314753; BAIDUID=A38E160C3D5C0A3AC6B1049ED0F7208C:FG=1; PSTM=1740579017; BIDUPSID=655665371040744D028AA8E5A82A881E; ab_sr=1.0.1_ODlkNTBkMTlhYTNhODkyZjEyOWQ4NDNiMDFkMDIzNzRhYjBlZDM3MWY1MzE0Y2Y4MjYxOGM1ZmZiNDIzNjkwMWI5OTk5ZDU5NzBmYTc0YzFlMmQyNGRmMzQyNTJhMzA3ZDQ4YTE1NDkzODA2OTYxNDc2NGE5NDcxZmFkNTE0ZDViY2JlNzIxYzg4NzI5ZDhkZWVkYjI5ZDllNWVjMzhiZg==; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=A38E160C3D5C0A3AC6B1049ED0F7208C:FG=1; B64_BOT=1; delPer=0; BD_CK_SAM=1; PSINO=3; BA_HECTOR=2g2ga5a08la10l8h8k0g818g0n3ahm1jse2gj1u; ZFY=xCmFSeDDUqyLQdNSCORn3s3JL3qZgOg:Bg0LHIz2v7Bg:C; BD_HOME=1; H_PS_PSSID=61027_61667_62169_62262_62279_62325_62346_62329_62249_62421; COOKIE_SESSION=564_15_7_7_7_14_0_5_6_5_0_1_1680_1734_0_0_1740668043_1740668066_1741099731%7C8%2349_45_1740666364%7C5; H_PS_645EC=2127OFAwhmtUFsvfOoOq4BTT13RmuTCvGHPazxfJcSz3EVmAtaKHMmOzC%2FU'
}


def baidu_deep_search(search_keyword, page_keywords, max_page):
    """
    尝试深度爬取页面内容，一些网页中不能直接获取营销组件链接，但有相关关键字可以利用
    :param search_keyword: 搜索关键字，如“北京+美容”等
    :param page_keywords: 网页关键字，如“在线咨询”，“联系我们”等
    :param max_page:搜索的最大页数
    """
    # 搜索是否出现“咨询”这个词语

    svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(service=svc)

    # selector   #\33 001 > div > div:nth-child(1) > div > div > h3 > div > a  当页前三个搜索结果可能为广告
    # selector   #\33 002 > div > div:nth-child(1) > div > div > h3 > div > a
    # selector   #\33 003 > div > div > div > div.c-gap-bottom-mini > h3 > div > a
    # selector   #\31 1 > div > div:nth-child(1) > div:nth-child(1) > h3 > a
    # selector   #\31 2 > div > div:nth-child(1) > div:nth-child(1) > h3 > a
    # selector   #\31 9 > div > div:nth-child(1) > div:nth-child(1) > h3 > a
    # selector   #\32 0 > div > div:nth-child(1) > div:nth-child(1) > h3 > a 当页最后一个搜索结果

    # 由selector确定每页爬取词条数量与是否翻页
    url_count = 1
    web_page = 0
    load_page = True
    for first in range(31, 35):
        for second in range(0, 9):
            if load_page:
                print('开始爬取第{}页'.format(web_page + 1))
                wait_seconds = random.uniform(1, 2)  # 等待时长秒
                print('开始等待{}秒'.format(wait_seconds))
                time.sleep(wait_seconds)  # 随机等待
                url = 'https://www.baidu.com/s?wd=' + \
                      search_keyword + '&pn=' + str(web_page * 10)
                driver.get(url)
                # 等待搜索结果加载完成
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h3.t"))
                )
                web_page += 1
                load_page = False
                pass

            selector = f'#\\{first} {second} > div > div:nth-child(1) > div:nth-child(1) > h3 > a'
            try:
                link = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"{url_count} :获取第{web_page}页，第{second}个搜索结果url成功:{link.get_attribute('href')}")
                # 打开搜索结果网页
                link.click()
                # 在新标签页中打开，切换到新标签页
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                # 在这里可以执行对新页面的操作，例如提取内容
                print("页面标题:", driver.title)

                # <a href="javascript:void(0);" onclick="openChat({eventSource: '我想咨询'});" rel="nofollow"><span style="color:red">【在线咨询】</span></a>
                for pk in page_keywords:
                    try:
                        # 页面内是否有关键字出现
                        button_xpath = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, f"//a[contains(text(),'${pk}')]"))
                        )
                        button_xpath.click()
                        print("通过xpath点击按钮成功！")
                        # todo 如果有弹窗
                    except Exception as e:
                        print(f"定位或点击按钮时出错：{e}")
                driver.close()  # 关闭当前标签页
                driver.switch_to.window(driver.window_handles[0])  # 切换到最初的标签页
            except (NoSuchElementException, Exception) as e:
                print(f"{url_count} :获取第{web_page}页，第{second}个搜索结果url失败:{NoSuchElementException}")
                load_page = True
            url_count += 1
            pass
    driver.quit()


if __name__ == '__main__':
    count = 0
    p_keywords = ["在线咨询", "联系我们", "点击咨询"]
    for city in citys:
        for need in needs:
            if count == 10:
                break
            count += 1

            try:
                s_keyword = f"{city.strip()}+{need}"
                print(s_keyword)
                baidu_deep_search(search_keyword=s_keyword, page_keywords=p_keywords, max_page=1)
            except Exception:
                traceback.print_exc()
                time.sleep(60)
                pass
