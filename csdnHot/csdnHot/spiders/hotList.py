import json
import scrapy

from csdnHot.items import HotList


class HotlistSpider(scrapy.Spider):
    name = 'hotList'
    allowed_domains = ['blog.csdn.net']
    current_page = 0
    start_urls = [
        f'https://blog.csdn.net/phoenix/web/blog/hotRank?page={current_page}&pageSize=25&child_channel=c%2Fc%2B%2B'
    ]

    def parse(self, response):
        items = json.loads(response.body)["data"]
        if len(items) > 0:
            for item in items:
                hot_list = HotList()
                hot_list["hotRankScore"] = item["hotRankScore"]
                hot_list["nickName"] = item["nickName"]
                hot_list["avatarUrl"] = item["avatarUrl"]
                hot_list["userName"] = item["userName"]
                hot_list["articleTitle"] = item["articleTitle"]
                hot_list["articleDetailUrl"] = item["articleDetailUrl"]
                hot_list["commentCount"] = item["commentCount"]
                hot_list["favorCount"] = item["favorCount"]
                hot_list["viewCount"] = item["viewCount"]
                yield hot_list
            # 如果还能获取到data，默认还有下一页
            self.current_page = self.current_page + 1
            next_page = f'https://blog.csdn.net/phoenix/web/blog/hotRank?page={self.current_page}&pageSize=25&child_channel=c%2Fc%2B%2B'
            yield scrapy.Request(next_page, callback=self.parse)
