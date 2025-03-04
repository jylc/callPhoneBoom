import requests  # 发送请求
import pandas as pd  # 存入csv数据
import time  # 等待间隔
import random  # 随机
import re  # 用正则表达式提取url
import traceback
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    driver = webdriver.Chrome()

    for page in range(max_page):
        print('开始爬取第{}页'.format(page + 1))
        wait_seconds = random.uniform(1, 2)  # 等待时长秒
        print('开始等待{}秒'.format(wait_seconds))
        time.sleep(wait_seconds)  # 随机等待
        url = 'https://www.baidu.com/s?wd=' + \
              search_keyword + '&pn=' + str(page * 10)
        driver.get(url)
        # 等待搜索结果加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.t"))
        )

        # 定位所有搜索结果的链接
        links = driver.find_elements(By.XPATH, '//h3/a')
        # 遍历链接并点击
        for link in links:
            try:
                link.click()
                # 在新标签页中打开，切换到新标签页
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                # 在这里可以执行对新页面的操作，例如提取内容
                print("页面标题:", driver.title)

                # 页面内搜索关键字
                for keyword in page_keywords:
                    try:
                        button_xpath = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, f"//button[contains(.,{keyword})]")))
                        button_xpath.click()
                        print("通过xpath点击按钮成功！")
                        # todo 如果有弹窗
                    except Exception as e:
                        print(f"定位或点击按钮时出错：{e}")

                driver.close()  # 关闭当前标签页
                driver.switch_to.window(driver.window_handles[0])  # 切换到最初的标签页
            except Exception as e:
                print(f"点击链接时出错：{e}")
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
