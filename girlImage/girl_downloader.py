import os
import re
import threading

import requests
import parsel

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
}


def open_url(_url, _path):
    html = requests.request("GET", _url, headers=headers).text
    images = parsel.Selector(html).xpath("//*[@class=\"tl_article_content\"]/figure/img/@src").extract()
    if not os.path.exists(_path):
        os.mkdir(_path)
        for index, image in enumerate(images):
            download_image("https://telegra.ph/" + image, index + 1, _path)
    else:
        print(f"{_path} 已存在跳过")
        pass


# 下载图片到指定目录
def download_image(image_url, index, _path):
    filename = image_url.split("/")[-1]
    suffix = filename.split(".")[-1]
    img_data = requests.request("GET", image_url, headers=headers).content
    with open(f"{_path}/{index}.{suffix}", 'wb') as f:
        print('下载图片 ', filename)
        f.write(img_data)


if __name__ == '__main__':
    path = "D:\\Downloads\\测试抓取网站\\图片\\"
    with open("girls.txt", encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
        for line in lines:
            reg = re.compile('(.*)\((https.*)\)')
            reg_match = reg.match(line)
            name = reg_match.group(1).strip()
            url = reg_match.group(2)
            print(f"开始下载 {name} --> {url}")
            thread = threading.Thread(target=open_url, args=[url, path + name])
            thread.start()
