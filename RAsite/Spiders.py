import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from CSPtool.models import Rating, Review, CSP
from django.db import models
import datetime

class ReviewSpider(scrapy.Spider):
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
        for sel in response.xpath('//div[@class ="node node-solution-review node-teaser node-feedback clearfix"]'):
            # Find the ID number of the post
            idNumber = sel.xpath('@id').extract()
            idNumber = int(idNumber[0].replace('review-', ''))

            # If the id is already in our database, ignore it.
            if Review.objects.filter(idNum = idNumber).exists():
                #print(" #@#@#@#@#@# Duplicate entry #@#@#@#@#@#")
                continue # effectively ignoring this entry
            else:
                #print(" #@#@#@#@#@# -- New entry -- #@#@#@#@#@#")
                pass

            # Find the name of the CSP
            CSPname = response.xpath('//h1/text()').extract()
            CSPname = CSPname[0].replace('\n','')[0:-1]

            # If it's in our database, hook this too it, if not, create the CSP
            if CSP.objects.filter(name=CSPname).exists():
                thisCSP = CSP.objects.get(name=CSPname)
            else:
                thisCSP = CSP(name = CSPname)
                thisCSP.save()

            # Create the new review and rating
            rev = Review(idNum = idNumber, CSP = thisCSP)
            rat = Rating(idNum = idNumber, CSP = thisCSP)

            # Get the review text and put in the review
            reviewtext = sel.xpath('div[@class="row row-custom "]/div/div/div[@class="col-52 project-col"]/h2[@class="hidden-xs"]/div[@class="field field-name-field-fdb-client-quote field-type-text-long field-label-hidden"]/div/div/p/text()').extract()
            reviewtext = reviewtext[0].replace('\"','')
            rev.plaintext = reviewtext

            # Get the date and put it in the rating AND the review
            datestring = sel.xpath('div[@class ="row row-custom "]/div/div/div[@class="col-52 project-col"]/h5[@class="date hidden-xs"]/text()').extract()
            datestring = datestring[0].replace('\n', '')
            rev.dateMade = datetime.datetime.strptime(datestring, "%b %d, %Y ").date()
            rat.dateMade = rev.dateMade

            # Get the location, if it exists, and put it in the rating AND review
            locstring = sel.xpath('div[@class ="row row-custom "]/div/div/div[@class = "review-mobile-cp hideon_active"]/div[@class="col-24 reviewer-col"]/div[@class="group-fdb-interview hidden-xs"]/div[@class="field field-name-field-fdb-location field-type-text field-label-hidden field-label-inline clearfix"]/div[@class="field-items"]/div/text()').extract()
            if(len(locstring)):
                locstring = locstring[0].replace('\n','')
                rev.locMade = locstring
                rat.locMade = locstring

            starsNum = sel.xpath('div[@class="row row-custom "]/div/div/div[@class ="col-24 review-col"]/div/div/div/div/div[@class="field field-name-field-fdb-overall-rating field-type-fivestar field-label-hidden"]/div/div/div/div/div/p/span/text()').extract()
            ratingPercent = (float(starsNum[0])/5.0)*100
            rat.value = ratingPercent

            rat.save()
            rev.save()

            yield None

        nextpage_url = response.xpath('//li[@class ="pager-next last"]/a/@href').extract()
        if nextpage_url:
            next_href = nextpage_url[0]
            nextpage_url = 'https://clutch.co' + next_href
            request = scrapy.Request(url = nextpage_url)
            yield request 
