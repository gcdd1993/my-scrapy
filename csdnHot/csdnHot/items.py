from scrapy import Field, Item


class HotList(Item):
    hotRankScore = Field()
    nickName = Field()
    avatarUrl = Field()
    userName = Field()
    articleTitle = Field()
    articleDetailUrl = Field()
    commentCount = Field()
    favorCount = Field()
    viewCount = Field()
