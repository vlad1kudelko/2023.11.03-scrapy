import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [ 'https://www.sapphire.ru' ]

    def parse(self, response):
        if response.url.split('/')[-1] == 'goodsinfo.html':
            yield {
                'url':          response.url,
                'title_red':    response.css('h1::text').get(),
                'path':         ' - '.join(response.css('.work_path li a span::text').getall()),
                'img':          response.css('.fancybox img::attr("src")').get(),
                'artic':        response.css('.artgd b:nth-child(1)::text').get().strip(),
                #  'price_old':    '-',
                'price':        response.css('div[itemprop="offers"] span::text').get(),
                'title_blue':   response.css('#gtext font b font::text').get(),
                'descr':        ''.join(response.css('#gtext::text').getall()).strip(),
            }
        else:
            catalog = response.css('a::attr("href")').getall()
            catalog = list(filter(lambda x: ('/catalog.html' in x) or ('/goodsinfo.html' in x), catalog))
            for item in catalog:
                yield response.follow(item, self.parse)
