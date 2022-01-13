#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
木瓜漫画爬取
"""
from concurrent.futures.thread import ThreadPoolExecutor

import requests
import os
from lxml import html

DOMAIN = "https://img.78te.com"


def parse_chapter(homepage_url):
    """
    解析章节列表

    :param homepage_url:
    :return: []
    """
    content = html.fromstring(s.get(homepage_url).content)
    return content.xpath('//*[@id="detail-list-select"]/li/a')


def parse_detail(chapter_url):
    """
    解析漫画正文

    :param chapter_url:
    :return: []
    """
    content = html.fromstring(s.get(chapter_url).content)
    return content.xpath('//*[@class="comicpage"]/div/img/@data-original')


# 下载图片到指定目录
def download_image(image_url, _path):
    if not os.path.exists(_path):
        os.makedirs(_path)
    filename = image_url.split("/")[-1]
    img_path = f"{_path}/{filename}"
    try:
        if os.path.exists(img_path):
            pass
            # print(f"{filename} is already downloaded.")
        else:
            print(f"正在下载 {image_url} -> {img_path}")
            img_data = requests.get(image_url).content
            with open(f"{img_path}", 'wb') as _f:
                # print('下载图片', filename)
                _f.write(img_data)
    except:
        print(f"{image_url} 下载失败...")


if __name__ == '__main__':
    s = requests.session()
    # 8线程的线程池
    pool = ThreadPoolExecutor(max_workers=4)
    path = "D:\\Downloads\\MT韩漫大合集\\恋爱辅助器(超级作弊器)"

    for chapter in parse_chapter(f"{DOMAIN}/cartoon/1229"):
        href = chapter.xpath("@href")[0]
        title = chapter.xpath("text()")[0]
        print(f"{title} -> {href}")
        imgs = parse_detail(f"{DOMAIN}{href}")

        for img in imgs:
            pool.submit(download_image, img, path + "/" + title)
