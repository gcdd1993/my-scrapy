# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanHotMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # - 电影名称
    title = scrapy.Field()
    # - 电影Logo
    cover = scrapy.Field()
    # - 上映年度
    release_year = scrapy.Field()
    # - 导演
    director = scrapy.Field()
    # - 编剧
    scenarist = scrapy.Field()
    # - 主演
    starring = scrapy.Field()
    # - 类型
    type = scrapy.Field()
    # - 制片国家/地区
    country_region = scrapy.Field()
    # - 语言
    language = scrapy.Field()
    # - 上映日期
    release_date = scrapy.Field()
    # - 片长
    length = scrapy.Field()
    # - 又名
    alias_name = scrapy.Field()
    # - `IMDb`
    imdb = scrapy.Field()
    # - 豆瓣评分
    rate = scrapy.Field()
    # - 评价人数
    comment_number = scrapy.Field()
