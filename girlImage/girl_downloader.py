import os
from urllib.parse import unquote

import parsel
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
}


def open_url(_url, _path):
    html = requests.request("GET", _url, headers=headers).text
    images = parsel.Selector(html).xpath("//*[@class=\"tl_article_content\"]/figure/img/@src").extract()
    if not os.path.exists(_path):
        os.makedirs(_path)
    for index, image in enumerate(images):
        download_image("https://telegra.ph/" + image, index + 1, _path)


# 下载图片到指定目录
def download_image(image_url, index, _path):
    filename = image_url.split("/")[-1]
    suffix = filename.split(".")[-1]
    img_data = requests.request("GET", image_url, headers=headers).content
    img_path = f"{_path}/{index}.{suffix}"
    if os.path.exists(img_path):
        print(f"{filename} is already downloaded.")
    else:
        with open(f"{_path}/{index}.{suffix}", 'wb') as _f:
            print('下载图片', filename)
            _f.write(img_data)


def parse_tg_export_html(html_path):
    """
    解析从TG频道导出的消息历史
    :param html_path: HTML文件路径
    :return: ["url"]
    """
    data = []
    with open(html_path, "r", encoding="utf-8") as _f:
        dom = etree.HTML(_f.read())
        a_list = dom.xpath('//div[@class="text"]/a')
        for a in a_list:
            data.append({
                "name": unquote(a.xpath("text()")[0].replace('https://telegra.ph/', '')),
                "url": a.xpath("@href")[0]
            })
    return data


def start(html_path):
    item_list = parse_tg_export_html(html_path)
    path = "图片/"
    if not os.path.exists(path):
        os.makedirs(path)
    for item in item_list:
        name = item['name']
        url = item['url']
        print(f"开始下载 {name} --> {url}")
        open_url(url, path + name)


if __name__ == '__main__':
    source = ['messages.html', 'messages2.html']
    for s in source:
        start(s)
