# -*- coding: UTF-8 -*-
"""
Author: Ethan Chai
Date: 2022/8/25 17:02

input:
output:

Short Description:
Change History:

"""
import requests
from lxml import etree

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62"
}
BASE_DOMAIN = "http://www.dytt8.net"


def get_response(url):
    """
    请求url获取响应
    :param url: 请求接口url
    :return: 响应 html
    """
    response = requests.get(url, headers=HEADERS)  # print(response.content.decode('gbk'))
    if response.ok:
        return response.content.decode("gbk")  # 拿到数据，，再解码


def get_detail_url(url):
    """
    获取详情页url
    :param url:
    :return:
    """
    response = get_response(url)
    html = etree.HTML(response)
    href_list = html.xpath("//table[@class='tbspan']//a/@href")
    # detail_urls = map(lambda url_: BASE_DOMAIN + url_, detail_urls)
    detail_urls = [BASE_DOMAIN + href for href in href_list]
    return detail_urls


def parse_detail_page(url):
    movie = {}
    response = get_response(url)
    html = etree.HTML(response)

    # 标题
    movie['title'] = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    # 封面
    movie['cover'] = html.xpath('//img/@src')[0]
    # 信息
    infos = html.xpath('//div[@id = "Zoom"]//text()')
    for index, info in enumerate(infos):
        if info.startswith('◎年　　代'):
            info = info.replace('◎年　　代', '').strip()
            movie['year'] = info
        elif info.startswith('◎产　　地'):
            info = info.replace('◎产　　地', '').strip()
            movie['country'] = info
        elif info.startswith('◎类　　别'):
            info = info.replace('◎类　　别', '').strip()
            movie['category'] = info
        elif info.startswith('◎语　　言'):
            info = info.replace('◎语　　言', '').strip()
            movie['language'] = info
        elif info.startswith('◎字　　幕'):
            info = info.replace('◎字　　幕', '').strip()
            movie['sub_title'] = info
        elif info.startswith('◎上映日期'):
            info = info.replace('◎上映日期', '').strip()
            movie['release_time'] = info
        elif info.startswith('◎豆瓣评分'):
            info = info.replace('◎豆瓣评分', '').strip()
            movie['douban_score'] = info
        elif info.startswith('◎片　　长'):
            info = info.replace('◎片　　长', '').strip()
            movie['length'] = info
        elif info.startswith('◎导　　演'):
            info = info.replace('◎导　　演', '').strip()
            movie['director'] = info
        elif info.startswith('◎演　　员'):
            info = info.replace('◎演　　员', '').strip()
            actors = []
            actors.append(info)
            for x in range(index + 1, len(infos)):
                actor = infos[x].strip()
                if actor.startswith('◎'):
                    break
                actors.append(actor)
                movie['actors'] = actors
        elif info.startswith("◎简　　介"):
            info = info.replace('◎简　　介', '').strip()
            profiles = []
            # profiles.append(info)
            for x in range(index + 1, len(infos)):
                profile = infos[x].strip()
                if profile.startswith("磁力链"):
                    break
                profiles.append(profile)
                movie['profiles'] = profiles
    # 下载地址
    # download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    # movie['download_url'] = download_url
    # 观看地址
    movie['watch_url'] = url
    print("详情信息：", movie)

    return movie


movies = []


def spider():
    base_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for x in range(1, 2):  # how much page depend on you
        url = base_url.format(x)
        detail_urls = get_detail_url(url)
        for detail_url in detail_urls:
            print("详情页地址：", detail_url)
            movie = parse_detail_page(detail_url)
            movies.append(movie)


if __name__ == '__main__':
    spider()
    with open('movies.Txt', 'a', encoding='utf-8') as f:
        for movie in movies:
            f.write("=" * 30)
            f.write('\n' * 2)
            for (key, value) in movie.items():
                if (key == 'actors'):
                    f.write('actors :{}'.format(value))
                    f.write('\n')
                elif (key == 'profiles'):
                    f.write('profiles :{}'.format(value))
                    f.write('\n')
                else:
                    f.write(key + ":" + value)
                    f.write('\n')
            f.write('\n' * 3)
