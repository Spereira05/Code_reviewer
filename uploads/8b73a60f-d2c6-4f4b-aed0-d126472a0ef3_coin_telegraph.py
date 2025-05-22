import scrapy

class coin_telegraph_spider(scrapy.Spider):
    name = "coin_telegraph"
    start_urls = ["https://cointelegraph.com/"] 

    def parse(self, response):
        # Keep track of processed URLs to avoid duplicates
        processed_urls = set()
        
        # Find all anchor elements that link to news articles
        news_anchors = response.xpath('//a[contains(@href, "/news/")]')
        
        for anchor in news_anchors:
            # Get the href attribute
            link = anchor.xpath('@href').get()
            
            # Skip if we've already processed this URL
            if link in processed_urls:
                continue
                
            processed_urls.add(link)
            full_url = response.urljoin(link)
            
            # Extract the text directly from the anchor element
            title = anchor.xpath('string(.)').get() or anchor.css('*::text').get()
            
            # Clean up the title
            if title:
                title = title.strip()
                # Remove excessive whitespace
                title = ' '.join(title.split())
            
            # Only yield if we have meaningful content
            if title and len(title) > 3:  # Avoid empty or very short titles
                yield {
                    "title": title,
                    "url": full_url,
                    "category": "News"
                }
        
        # Find next page link
        next_page = response.css("a.next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
