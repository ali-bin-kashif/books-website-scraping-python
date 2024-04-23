import scrapy
import pandas as pd


class BooksSpider(scrapy.Spider):
    name = "books"
    
    # Global list of books
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

        cards = response.css('.product_pod')
        
        # Looping in cards to get info
        for card in cards:

            book_title = card.css('h3>a::attr(title)').get()
            
            product_price = card.css('.product_price>p::text').get()
            
            star_rating = card.css('p::attr(class)').get()
            
            # Creating dictionary which then can be saved as csv or json files
            books_dict = {
                'Title' : book_title,
                'Price' : product_price,
                'Rating' : star_rating.split()[1],
                'Category' : title
            }
            
            # Appending in the global book list
            BooksSpider.books.append(books_dict)
        
        # Get next button if present on page
        next_button = response.css('.next')
        
        # If next button is present crawl the next page and scrape the data
        if(next_button.get() != None):
            next_path = next_button.css('a::attr(href)').get()
            path_split = response.url.split('/')[0:7]
            next_url = "/".join(path_split) + "/" + next_path
            yield response.follow(url=next_url, callback=self.page_parse)
            
        # Creating a dataframe with the global list and exporting CSV File
        data = pd.DataFrame(BooksSpider.books)
        data.to_csv('scraped_data/books_data.csv', index=False)