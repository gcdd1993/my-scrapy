import scrapy

from ruike1_list.items import Ruike1ListItem


class PostListSpider(scrapy.Spider):
    name = 'post_list'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
    allowed_domains = ['www.ruike1.com']
    current_page = 1
    max_page = 325
    start_urls = [f'https://www.ruike1.com/forum-47-{current_page}.html']

    def parse(self, response, **kwargs):
        tbodys = response.xpath('//*[@summary="forum_47"]//tbody')
        for tbody in tbodys:
            meta = Ruike1ListItem()
            self.__set_title(meta, tbody)
            self.__set_url(meta, tbody)
            # self.__set_author(meta, tbody)
            # self.__set_reply_num(meta, tbody)
            # self.__set_view_num(meta, tbody)
            yield meta
        self.current_page += 1
        if self.current_page > self.max_page:
            return
        next_page = f'https://www.ruike1.com/forum-47-{self.current_page}.html'
        yield scrapy.Request(next_page,
                             headers={'Referer': f'https://www.ruike1.com/forum-47-{self.current_page - 1}.html'})

    def __set_title(self, meta, response):
        xpath = 'tr/th[@class="new"]/a[2]/text()'
        match = response.xpath(xpath).get()
        if match:
            meta["title"] = match
        else:
            xpath = 'tr/th[@class="common"]/a[2]/text()'
            match = response.xpath(xpath).get()
            if match:
                meta["title"] = match
        return meta

    def __set_url(self, meta, response):
        xpath = 'tr/th[@class="new"]/a[2]/@href'
        match = response.xpath(xpath).get()
        if match:
            meta["url"] = "https://www.ruike1.com/" + match
        else:
            xpath = 'tr/th[@class="common"]/a[2]/@href'
            match = response.xpath(xpath).get()
            if match:
                meta["url"] = "https://www.ruike1.com/" + match
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
