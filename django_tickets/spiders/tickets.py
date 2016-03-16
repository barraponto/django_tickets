# -*- coding: utf-8 -*-
import scrapy


class TicketsSpider(scrapy.Spider):
    name = "tickets"
    allowed_domains = ["code.djangoproject.com"]
    start_urls = (
        'https://code.djangoproject.com/query',
    )

    def parse(self, response):
        for ticket_url in response.css('td.id a::attr("href")').extract():
            yield scrapy.Request(response.urljoin(ticket_url),
                                 callback=self.parse_ticket)

        for page_url in response.css('.paging a::attr("href")').extract():
            yield scrapy.Request(response.urljoin(page_url))

    def parse_ticket(self, response):
        yield {
            'title': response.css('.summary::text').extract_first(),
            'reporter': response.css('#h_reporter + .searchable a::text').extract_first()
        }
