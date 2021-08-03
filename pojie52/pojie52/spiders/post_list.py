import scrapy

from pojie52.items import Pojie52Item


class PostListSpider(scrapy.Spider):
    name = 'post_list'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    allowed_domains = ['www.52pojie.cn']
    current_page = 1
    max_page = 1000
    start_urls = [f'https://www.52pojie.cn/forum-16-{current_page}.html']

    def parse(self, response, **kwargs):
        tbodys = response.xpath('//*[@summary="forum_16"]//tbody')
        for tbody in tbodys:
            meta = Pojie52Item()
            self.__set_title(meta, tbody)
            self.__set_url(meta, tbody)
            # self.__set_author(meta, tbody)
            # self.__set_reply_num(meta, tbody)
            # self.__set_view_num(meta, tbody)
            yield meta
        self.current_page += 1
        if self.current_page > self.max_page:
            return
        next_page = f'https://www.52pojie.cn/forum-16-{self.current_page}.html'
        yield scrapy.Request(next_page,
                             headers={'Referer': f'https://www.52pojie.cn/forum-16-{self.current_page - 1}.html'})

    def __set_title(self, meta, response):
        xpath = 'tr/th[@class="new"]/a[2]/text()'
        match = response.xpath(xpath).get()
        print(match)
        if match:
            meta["title"] = match
        else:
            xpath = 'tr/th[@class="common"]/a[2]/text()'
            match = response.xpath(xpath).get()
            if match:
                meta["title"] = match
            else:
                xpath = 'tr/th[@class="lock"]/a[2]/text()'
                match = response.xpath(xpath).get()
                if match:
                    meta["title"] = match
        return meta

    def __set_url(self, meta, response):
        xpath = 'tr/th[@class="new"]/a[2]/@href'
        match = response.xpath(xpath).get()
        if match:
            meta["url"] = "https://www.52pojie.cn/" + match
        else:
            xpath = 'tr/th[@class="common"]/a[2]/@href'
            match = response.xpath(xpath).get()
            if match:
                meta["url"] = "https://www.52pojie.cn/" + match
            else:
                xpath = 'tr/th[@class="lock"]/a[2]/@href'
                match = response.xpath(xpath).get()
                if match:
                    meta["url"] = "https://www.52pojie.cn/" + match
        return meta

    def __set_author(self, meta, response):
        xpath = 'tr/td[@class="by"][1]/cite/a/text()'
        match = response.xpath(xpath).get()
        if match:
            meta["author"] = match
        return meta

    def __set_reply_num(self, meta, response):
        xpath = 'tr/td[@class="num"][1]/a/text()'
        match = response.xpath(xpath).get()
        if match:
            meta["reply_num"] = match
        return meta

    def __set_view_num(self, meta, response):
        xpath = 'tr/td[@class="num"][1]/em/text()'
        match = response.xpath(xpath).get()
        if match:
            meta["view_num"] = match
        return meta
