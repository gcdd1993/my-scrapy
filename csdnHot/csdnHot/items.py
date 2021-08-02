from scrapy import Field, Item


class HotList(Item):
    hot_rank_score = Field()
    nick_name = Field()
    avatar_url = Field()
    username = Field()
    article_title = Field()
    article_detail_url = Field()
    comment_count = Field()
    favor_count = Field()
    view_count = Field()
