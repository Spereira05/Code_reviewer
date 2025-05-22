import scrapy
# from pathlib import Path

class testSpider(scrapy.Spider):
    name = "test"
    # shortcut if just passing the urls
    start_urls = [
        "https://cointelegraph.com/",
    ]
    # def start_requests(self):
    #     url = "https://quotes.toscrape.com/"
    #     tag = getattr(self, "tag", None)
    #     if tag is not None:
    #         url = url + "tag/" + tag
    #     yield scrapy.Request(url, self.parse)
        
    def parse(self, response):
        for quote in response.css("div"):
            yield {
                "Title": quote.css("a.href::text").get(),
            } 
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
            
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            # two ways of following links
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)
        # pass a selector instead of a string:
        # for href in response.css("ul.pager a::attr(href)"):
        #     yield response.follow(href, callback=self.parse)
        # shortcut for <a> elements:
        # for a in response.css("ul.pager a"):
        #     yield response.follow(a, callback=self.parse)
        # 
        # multiple requests from an iterable:
        # anchors = response.css("ul.pager a")
        #     yield from response.follow_all(anchors, callback=self.parse)
        # shortcut for it:
        # yield from response.follow_all(css="ul.pager a", callback=self.parse)
