# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class HockeyReferenceSpider(scrapy.Spider):
    name = 'hockey_reference'
    download_delay = 3

    def start_requests(self):
        # For the URLs to scrape, 2018 denotes the 2017-2018 season
        # This is required to ensure that cur_year represents the latest season
        base_url = 'https://www.hockey-reference.com/leagues/NHL_'
        suffix_url = '_games.html'

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
        
        start_urls = [base_url + str(year) + suffix_url for year in
            range(start_year, end_year + 1)]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def __parse_data_from_row(self, row):
        """
        Given a scrapy.Selector representing a row of data from a table on the
        Hockey-Reference website, return a dict representing that data. A row
        represents the score for one game.

        :param row: scrapy.Selector representing a row of data
        :returns: dict which contains the teams, date, and final score
        """
        # TODO: Turn strs to int and return dict
        date_string = row.css('th a::text').extract_first()
        visitor_team = row.css('td[data-stat="visitor_team_name"] a::text')\
            .extract_first()
        visitor_goals = row.css('td[data-stat="visitor_goals"]::text')\
            .extract_first()
        home_team = row.css('td[data-stat="home_team_name"] a::text')\
            .extract_first()
        home_goals = row.css('td[data-stat="home_goals"]::text')\
            .extract_first()


    def parse(self, response):
        reg_season_table = response.css('#all_games #games tbody tr')
        playoffs_table = response.css('#all_games_playoffs #games_playoffs '
            'tbody tr')
        
        # TODO: pull data from the regular season table and the playoffs table