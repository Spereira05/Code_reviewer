import scrapy


class CryptonewsSpider(scrapy.Spider):
    name = "cryptoNews"
    allowed_domains = ["crypto.news"]
    start_urls = ["https://crypto.news"]

    def parse(self, response):
        for news in response('div.home-latest-news-item__list'):
            yield {
                    'title' : news.css('span.home-latest-news-item__title::text').get(),
                    'url' : news.css('a.home-latest-news-item__title').attrib['href'],
                    'time' : news.css('time.home-latest-news-item__date::text').get(),
            }
