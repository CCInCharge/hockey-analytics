# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class HockeyReferenceSpider(scrapy.Spider):
    name = 'hockey_reference'
    download_delay = 3
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.HockeyReferencePipeline': 1,
        }
    }

    def start_requests(self):
        # TODO: docstring for this method
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
            '_games.html' for year in
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
        date_string = row.css('th a::text').extract_first()
        game_link = 'https://www.hockey-reference.com' + \
                row.css('th a::attr(href)').extract_first()
        visitor_team = row.css('td[data-stat="visitor_team_name"] a::text')\
                .extract_first()
        visitor_goals = row.css('td[data-stat="visitor_goals"]::text')\
                .extract_first()
        home_team = row.css('td[data-stat="home_team_name"] a::text')\
                .extract_first()
        home_goals = row.css('td[data-stat="home_goals"]::text')\
                .extract_first()
        
        visitor_team_abbrv_str = row.css('td[data-stat="visitor_team_name"] '
                'a::attr(href)').extract_first()
        home_team_abbrv_str = row.css('td[data-stat="home_team_name"] '
                'a::attr(href)').extract_first() 
        tokenize_visitor = visitor_team_abbrv_str.split("/")
        tokenize_home = home_team_abbrv_str.split("/")
        visitor_abbrv = tokenize_visitor[-2]
        home_abbrv = tokenize_home[-2]
        visitor_year = int(tokenize_visitor[-1][0:4])
        home_year = int(tokenize_home[-1][0:4])

        return {"date_string": date_string,
                "game_link": game_link,
                "visitor_team": visitor_team,
                "visitor_abbrv": visitor_abbrv,
                "visitor_year": visitor_year,
                "visitor_goals": int(visitor_goals),
                "home_team": home_team,
                "home_abbrv": home_abbrv,
                "home_year": home_year,
                "home_goals": int(home_goals)}

    def parse(self, response):
        reg_season_table = response.css('#all_games #games tbody tr')

        # TODO: Save playoff record
        playoffs_table = response.css('#all_games_playoffs #games_playoffs '
            'tbody tr')
        
        output = []
        for row in reg_season_table:
            output.append(self.__parse_data_from_row(row))
        
        return output