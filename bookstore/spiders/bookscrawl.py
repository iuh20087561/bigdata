import scrapy
from bookstore.items import BookstoreItem

class BookscrawlSpider(scrapy.Spider):
    name = "bookscrawl"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # bookList = response.xpath('normalize-space(string(/html/body/div/div/div/div/section/div/descendant::ol/li/article/div/a/@href))').getall()
        bookList = response.xpath('/html/body/div/div/div/div/section/div/descendant::ol/li/article/div/a/@href').getall()
        for book in bookList:
            item = BookstoreItem()
            item['bookURL'] = response.urljoin(book)
            # string3 = string1 + string 2 
            request = scrapy.Request(url = response.urljoin(book), callback=self.bookDetail)
            request.meta['datacourse'] = item

            yield request
        
        nextButton = response.xpath('/html/body/div/div/div/div/section/div[2]/div/ul/li[last()]/a/@href').get()

        if(nextButton != ''):
            yield scrapy.Request(url=response.urljoin(nextButton), callback=self.parse)
        

    def bookDetail(self, response):
        item = response.meta['datacourse']
        item['bookName'] = response.xpath('normalize-space(string(/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/h1))').get()
        item['price'] = response.xpath('normalize-space(string(/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[1]))').get()
        item['stock'] = response.xpath('normalize-space(string(/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[2]))').get()
        item['descrip'] = response.xpath('normalize-space(string(/html/body/div/div/div[2]/div[2]/article/p))').get()
        item['rating'] = response.xpath('normalize-space(string(/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[3]/@class))').get()
        item['rating'] = item['rating'].split(' ')[-1]
        
    
        yield item
            
