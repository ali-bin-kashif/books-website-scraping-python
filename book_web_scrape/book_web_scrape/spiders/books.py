import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    def start_requests(self):
        
        main_url = "https://books.toscrape.com/"
        
        yield scrapy.Request(url=main_url, callback=self.main_parse)

    def main_parse(self, response):
        # print(response.url)
        sidebar_pages_paths = response.css('div.side_categories>ul>li>ul>li>a::attr(href)').getall()
        print(len(sidebar_pages_paths))
        for path in sidebar_pages_paths:
            url = 'https://books.toscrape.com/'+path
            yield response.follow(url=url, callback=self.page_parse)

    def page_parse(self, response):
        title = response.css('h1::text').get()
        print(title)
        cards = response.css('.product_pod')
        # for card in cards:
            
        # print(title)