from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline

class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/']
    
    # リンクをたどるためのルールのリスト
    rules = {
        # トピックスのページのリンクをたどり、レスポンスをparse_topics()メソッドで処理する。
        Rule(LinkExtractor(allow='/pickup/\d+$'), callback='parse_topics')
    }
    
    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す
        """
        item = Headline()  # Headlineオブジェクトを作成。
        item['title'] = response.css('[data-ual-view-type="digest"] > a > p::text').get()  # タイトル
        item['body'] = response.css('[data-ual-view-type="digest"] > p').xpath('string()').get()  # 本文
        yield item  # Itemをyieldして、データを抽出する。