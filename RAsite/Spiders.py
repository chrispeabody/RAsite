import scrapy
from RASite.SpiderItems import CloudreviewsItem
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from CSPtool.models import Rating, Review

class ReviewSpider(BaseSpider):
    name = "Reviews"
    allowed_domains = ["clutch.co"]
    #allowed_domains = ["hostingreviews.io"]
    start_urls = ["https://clutch.co/cloud/profile/amazon-web-services-aws#reviews",
                  "https://clutch.co/cloud/profile/microsoft-azure#reviews",
                  "https://clutch.co/cloud/profile/google-cloud-platform#reviews",
                  "https://clutch.co/cloud/profile/ibm-cloud#reviews",
                  "https://clutch.co/cloud/profile/rackspace#reviews",
                  ]
    #start_urls = ["http://hostingreviews.io/web-hosting/amazon-web-services"]
    Rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class ="pager-next last"]/a',)), callback = "parse", follow = True),)
    def parse(self, response):
        #hxs = Selector(response)
        for sel in response.xpath('//div[@class="review-border only-1-line"]/div[@class="clearfix"]'):
            rev = Review()
            rat = Rating()

            rat['value']=sel.xpath('div[@class ="col-24 review-col"]/div/div/div/div/div[@class="field field-name-field-fdb-overall-rating field-type-fivestar field-label-hidden"]/div/div/div/div/div/p/span/text()').extract()
            rev['plaintext'] = sel.xpath('div[@class="col-52 project-col"]/h2[@class="hidden-xs"]/div[@class="field field-name-field-fdb-client-quote field-type-text-long field-label-hidden"]/div/div/p/text()').extract()
            rat['CSP'] = response.xpath('//h1/text()').extract()
            rev['CSP'] = rat['CSP']
            rat['dateMade'] = sel.xpath('div[@class="col-52 project-col"]/h5[@class="date hidden-xs"]/text()').extract()
            rev['dateMade'] = rat['dateMade']
            rat.save()
            rev.save()
            # yield rat
            # yield rev

            # item = CloudreviewsItem()
            # item['starRating']=sel.xpath('div[@class ="col-24 review-col"]/div/div/div/div/div[@class="field field-name-field-fdb-overall-rating field-type-fivestar field-label-hidden"]/div/div/div/div/div/p/span/text()').extract()
            # item['reviewText'] = sel.xpath('div[@class="col-52 project-col"]/h2[@class="hidden-xs"]/div[@class="field field-name-field-fdb-client-quote field-type-text-long field-label-hidden"]/div/div/p/text()').extract()
            # item['CloudProvider'] = response.xpath('//h1/text()').extract()
            # item['timeStamp'] = sel.xpath('div[@class="col-52 project-col"]/h5[@class="date hidden-xs"]/text()').extract()
            # yield item


        nextpage_url = response.xpath('//li[@class ="pager-next last"]/a/@href').extract()
        if nextpage_url:
            next_href = nextpage_url[0]
            nextpage_url = 'https://clutch.co' + next_href
            request = scrapy.Request(url = nextpage_url)
            yield request 
