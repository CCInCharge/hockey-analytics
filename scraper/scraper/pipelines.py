# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
import configparser
from scraper.settings import PROJECT_ROOT, DB_CONFIG_PATH

class TeamAbbrvPipeline(object):
    def open_spider(self, spider):
        config = configparser.ConfigParser()
        config.read(DB_CONFIG_PATH)
        hostname = config['database']['hostname']
        user = config['database']['user']
        password = config['database']['password']
        database = config['database']['database_name']
        
        self.conn = mysql.connector.connect(user=user, password=password,
                host=hostname, database=database)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute("INSERT IGNORE INTO teams (id, year, name) "
                "VALUES (%s, %s, %s)",
                (str(item['year']) + ' ' + item['abbrv'],
                item['year'], item['name']))
        self.conn.commit()
        return item

# TODO: Setup message broker as output for links from hockey_reference spider
class HockeyReferencePipeline(object):
    def open_spider(self, spider):
        config = configparser.ConfigParser()
        config.read(DB_CONFIG_PATH)
        hostname = config['database']['hostname']
        user = config['database']['user']
        password = config['database']['password']
        database = config['database']['database_name']

        self.conn = mysql.connector.connect(user=user, password=password,
                host=hostname, database=database)
        self.cur = self.conn.cursor()
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # TODO: Test this query
        self.cur.execute("INSERT IGNORE INTO games (game_date, url, "
                "away_team_id, home_team_id, away_team_goals, "
                "home_team_goals) VALUES (%s, %s, %s, %s, %s, %s)",
                (item['date_string'], 
                item['url'], 
                str(item['visitor_year']) + ' '  + item['visitor_abbrv'],
                str(item['home_year']) + ' '  + item['home_abbrv'],
                item['visitor_goals'],
                item['home_goals']))
        self.conn.commit()
        return item