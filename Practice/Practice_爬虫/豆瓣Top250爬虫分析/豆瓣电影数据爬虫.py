# -*- coding: UTF-8 -*-
import time
import requests
import pandas as pd
from lxml import etree
import random
from collections import defaultdict


user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def req_and_res(uri):
    headers = {
        "User-Agent": random.choice(user_agent_list)
    }
    response = requests.get(uri, headers=headers)
    if response.ok:
        res_html = etree.HTML(response.text)
        return res_html


result_data = defaultdict(list)

for i in range(10):
    url = f"https://movie.douban.com/top250?start={i * 25}&filter="
    try:
        html = req_and_res(uri=url)
        # 电影uri
        movie_uri_list = html.xpath('//ol[@class="grid_view"]/li/div/div/div/a/@href')
    except:
        print("哦吼，被反爬了！当前页面url -> ", url)
        break
    for movie_uri in movie_uri_list:
        # print(movie_uri)
        try:
            movie_html = req_and_res(movie_uri)
            name, year = movie_html.xpath('//div[@id="content"]/h1/span/text()')
        except:
            print("哦吼，被反爬了！当前电影url -> ", movie_uri)
            break
        # 电影名
        movie_name = name.split()[0]
        result_data["name"].append(movie_name)
        # 电影年份
        movie_year = year.replace("(", '').replace(")", '')
        result_data["year"].append(movie_year)
        # 导演
        director = movie_html.xpath('//div[@id="info"]/span/span[@class="attrs"]/a/text()')[0]
        result_data["director"].append(director)
        # 主演
        actor = movie_html.xpath('//div[@id="info"]/span[@class="actor"]/span/a/text()')
        result_data["actor"].append(actor)
        # 类型
        label = movie_html.xpath('//div[@id="info"]/span[@property="v:genre"]/text()')
        result_data["label"].append(label)
        # 评分
        score = movie_html.xpath('//div/strong[@class="ll rating_num"]/text()')[0]
        result_data["score"].append(score)
        # 评论人数
        rating_sum = movie_html.xpath('//div[@class="rating_sum"]/a/span[@property="v:votes"]/text()')[0]
        result_data["rating_sum"].append(rating_sum)
        # print(movie_name, movie_year, director, actor, label, score, rating_sum)

        time.sleep(15)

df = pd.DataFrame(result_data)
df.to_excel("DouBan.xlsx", encoding="utf-8", index=False)



