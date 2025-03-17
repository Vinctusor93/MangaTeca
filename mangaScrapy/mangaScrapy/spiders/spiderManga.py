import logging

import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor


class HackerNewsSpider(scrapy.Spider):
    name = "name"
    start_urls = [
        "https://www.mangabats.com/manga/one-piece"
    ]
    def parse(self, response):
        for manga in response.css("div.row"):
            logging.warning(manga)
            yield {
                "title": manga.css("div.row span a::text").get(),
                "url": manga.css("div.row span a::text").get(),
                "lastDate": manga.css("div.row span:nth-child(3)::text").get()
            }
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
# the wrapper to make it run more times
def run_spider(spider):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result