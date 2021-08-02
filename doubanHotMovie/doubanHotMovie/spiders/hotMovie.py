import json

import scrapy
from doubanHotMovie.items import DoubanHotMovieItem


class HotmovieSpider(scrapy.Spider):
    name = 'hotMovie'
    current_page = 0
    allowed_domains = ['movie.douban.com']
    start_urls = [
        f'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=time&page_limit=20&page_start={current_page}'
    ]

    def parse(self, response, **kwargs):
        items = json.loads(response.body)["subjects"]
        if len(items) > 0:
            for item in items:
                # 获取详情页链接
                detail_url = item['url']
                yield scrapy.Request(detail_url, callback=self.parse_item)
                # 如果还能获取到subjects，认为还有下一页
                # self.current_page = self.current_page + 1
                # next_page = f'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=time&page_limit=20&page_start={self.current_page}'
                # yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        """
        解析详情页，获取我们要的数据
        """
        item = DoubanHotMovieItem()
        item["title"] = self.safe_parse(response, '//*[@id="content"]/h1/span[1]/text()')
        item["cover"] = self.safe_parse(response, '//*[@id="mainpic"]/a/img/@src')
        item["release_year"] = self.safe_parse(response, '//*[@id="content"]/h1/span[2]/text()')
        item["director"] = self.safe_parse(response, '//*[@id="info"]/span[1]/span[2]/a/text()')
        item["scenarist"] = self.safe_parse(response, '//*[@id="info"]/span[2]/span[2]')
        item["starring"] = self.safe_parse(response, '//*[@id="info"]/span[3]/span[2]')
        item["type"] = self.safe_parse(response, '//*[@id="info"]/span[@property="v:genre"]/text()')
        item["country_region"] = self.safe_parse(response,
                                                 '//text()[preceding-sibling::span[text()="制片国家/地区:"]][following-sibling::br][1]')
        item["language"] = self.safe_parse(response,
                                           '//text()[preceding-sibling::span[text()="语言:"]][following-sibling::br][1]')
        item["release_date"] = self.safe_parse(response, '//*[@id="info"]/span[11]')
        item["length"] = self.safe_parse(response, '//*[@id="info"]/span[13]')
        item["alias_name"] = self.safe_parse(response,
                                             '//text()[preceding-sibling::span[text()="又名:"]][following-sibling::br][1]')
        item["imdb"] = self.safe_parse(response,
                                       '//text()[preceding-sibling::span[text()="IMDb:"]][following-sibling::br][1]')
        item["rate"] = self.safe_parse(response, '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        item["comment_number"] = self.safe_parse(response,
                                                 '//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')
        yield item

    def safe_parse(self, response, xpath):
        """
        因为详情页内容有的时候没有，防止出错，才这么写
        """
        matches = response.xpath(xpath).get()
        if matches:
            return matches
