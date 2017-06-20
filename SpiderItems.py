
import scrapy


class CloudreviewsItem(scrapy.Item):
    CloudProvider = scrapy.Field()
    starRating = scrapy.Field()
    reviewText = scrapy.Field()
    timeStamp = scrapy.Field()
    pass
