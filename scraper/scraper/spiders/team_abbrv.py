# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class TeamAbbrvSpider(scrapy.Spider):
    name = 'team_abbrv'
    download_delay = 3
    allowed_domains = ['https://www.hockey-reference.com/leagues/NHL_2000_standings.html']
    start_urls = ['http://https://www.hockey-reference.com/leagues/NHL_2000_standings.html/']

    def start_requests(self):
        # need to add attribute -a and start year and end year

        # For the URLs to scrape, 2018 denotes the 2017-2018 season
        # This is required to ensure that cur_year represents the latest season
        cur_month = datetime.now().month
        if cur_month >= 8:
            cur_year = datetime.now().year + 1
        else:
            cur_year = datetime.now().year
        start_year = int(getattr(self, 'start_year', cur_year))
        end_year = int(getattr(self, 'end_year', cur_year))

        if end_year < start_year:
            raise ValueError('end_year must be start_year or later')
        elif start_year < 2000:
            raise ValueError('end_year must be 2000 or later')
        
        start_urls = ['https://www.hockey-reference.com/leagues/NHL_' + 
            str(year) + 
            '_standings.html' for year in
            range(start_year, end_year + 1)]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def __parse_data_from_link(self, link):
        link_url = link.css("::attr(href)").extract_first()
        tokenize = link_url.split("/")
        
        abbrv = tokenize[-2]
        year = int(tokenize[-1][0:4])
        name = link.css("::text").extract_first()
        
        return {"abbrv": abbrv,
            "year": year,
            "name": name}

    def parse(self, response):
        eastern = response.css("#standings_EAS tbody .full_table th a")
        western = response.css("#standings_WES tbody .full_table th a")
        # TODO: Run this for every team and output to database
