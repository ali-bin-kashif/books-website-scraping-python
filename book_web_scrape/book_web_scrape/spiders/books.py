import scrapy
import pandas as pd


class BooksSpider(scrapy.Spider):
    name = "books"
    books = []
    def start_requests(self):
        
        # Book Website home page link
        main_url = "https://books.toscrape.com/"
        
        yield scrapy.Request(url=main_url, callback=self.main_parse)

    def main_parse(self, response):
        # Getting all the links in the side bar panel
        sidebar_pages_paths = response.css('div.side_categories>ul>li>ul>li>a::attr(href)').getall()

        
        # Crawl each web page one by one
        for path in sidebar_pages_paths:
            url = 'https://books.toscrape.com/'+path
            
            # Follow each page link and parse the response body the page_parse function
            yield response.follow(url=url, callback=self.page_parse)

    def page_parse(self, response):
        title = response.css('h1::text').get()
        # print(title)
        cards = response.css('.product_pod')
        # print('Books : ', len(cards))
        
        for card in cards:
            book_title = card.css('h3>a::attr(title)').get()
            
            product_price = card.css('.product_price>p::text').get()
            
            star_rating = card.css('p::attr(class)').get()
            
            books_dict = {
                'Title' : book_title,
                'Price' : product_price,
                'Rating' : star_rating.split()[1],
                'Category' : title
            }
            
            BooksSpider.books.append(books_dict)
            
            # img = card.css('.image_container img::attr(src)').get()
            # path = 'books.csv'
            # csv_file = open(path, 'a')
            # csv_file.write(book_title.replace(",",":") + "," + product_price[1:] + "," + star_rating.split()[1] + "," + title+"\n")

        data = pd.DataFrame(BooksSpider.books)
        data.to_csv('books.csv')