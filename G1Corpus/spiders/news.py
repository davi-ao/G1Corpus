import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = []

    def __init__(self):
        super(NewsSpider, self).__init__()

        for i in range(451, 501):
            self.start_urls.append('http://g1.globo.com/index/feed/pagina-' + str(i) + '.html')

    def parse(self, response):
        for href in [s.encode('ascii') for s in response.css('a.feed-post-link::attr(href)').extract()]:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

    @staticmethod
    def parse_news(response):
        title = response.css('.content-head__title::text').extract()

        if title:
            yield {
                'title': title,
                'subtitle': response.css('.content-head__subtitle::text').extract(),
                'text': response.css('.content-text__container::text').extract()
            }
