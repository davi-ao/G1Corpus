import scrapy
import json
import re


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    start_urls = []

    def __init__(self):
        super(CommentsSpider, self).__init__()

        for i in range(451, 501):
            self.start_urls.append('http://g1.globo.com/index/feed/pagina-' + str(i) + '.html')

    def parse(self, response):
        for href in [s.encode('ascii') for s in response.css('a.feed-post-link::attr(href)').extract()]:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

    def parse_news(self, response):
        link = "http://comentarios.globo.com/comentarios/" + re.search("COMENTARIOS_URI:\s\"[a-z1-9\/-]*\"", response.css('script[id=SETTINGS]').extract_first()).group(0).encode('ascii')[18:-1].replace('/', '@@') + "/" + re.search("COMENTARIOS_IDEXTERNO:\s\"[a-z0-9\/-]*\"", response.css('script[id=SETTINGS]').extract_first()).group(0).encode('ascii')[24:-1].replace('/', '@@') + "/" + response.url.replace('/', '@@') + "/shorturl/" + re.search("TITLE:\s\"[^\n]*\"", response.css('script[id=SETTINGS]').extract_first()).group(0).encode('latin-1')[8:-1] + "/1.json"
        yield scrapy.Request(response.urljoin(link), callback=self.parse_comment)

    def parse_comment(self, response):
        body = json.loads(response.body[28:-1])

        for itens in body['itens']:
            result = {
                'autor': itens['Usuario']['nome'],
                'texto': itens['texto']
            }

            for ir in itens['replies']:
                result['autor_resposta'] = ir['Usuario']['nome']
                result['texto_resposta'] = ir['texto']

            yield result
