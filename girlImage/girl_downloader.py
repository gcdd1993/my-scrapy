import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote

import parsel
import requests
from lxml import etree
from tqdm import trange

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
}


def open_url(_url, _base_path, _name):
    _path = _base_path + _name
    html = requests.request("GET", _url, headers=headers).text
    images = parsel.Selector(html).xpath("//*[@class=\"tl_article_content\"]/figure/img/@src").extract()
    if not os.path.exists(_path):
        os.makedirs(_path)
    for i in trange(len(images), postfix=f"正在下载 {_name}"):
        download_image(images[i], _path)


# 下载图片到指定目录
def download_image(image, _path):
    image_url = "https://telegra.ph"
    if "/" in image:
        image_url = f"{image_url}{image}"
    else:
        image_url = f"{image_url}/{image}"
    filename = image_url.split("/")[-1]
    img_path = f"{_path}/{filename}"
    try:
        if os.path.exists(img_path):
            pass
            # print(f"{filename} is already downloaded.")
        else:
            img_data = requests.request("GET", image_url, headers=headers).content
            with open(f"{img_path}", 'wb') as _f:
                # print('下载图片', filename)
                _f.write(img_data)
    except:
        print(f"{image_url} 下载失败...")


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
            prep = {
                "name": unquote(a.xpath("text()")[0].replace('https://telegra.ph/', '')),
                "url": a.xpath("@href")[0]
            }
            if "telegra.ph" in prep['url']:
                data.append(prep)
            else:
                print(f"丢弃 {prep}")
    return data


def start(html_path):
    item_list = parse_tg_export_html(html_path)
    path = "图片/"
    if not os.path.exists(path):
        os.makedirs(path)
    for item in item_list:
        name = item['name']
        url = item['url']
        # print(f"开始下载 {name} ")
        pool.submit(open_url, url, path, name)


if __name__ == '__main__':
    source = ['messages.html', 'messages2.html']
    # 8线程的线程池
    pool = ThreadPoolExecutor(max_workers=8)
    for s in source:
        start(s)
