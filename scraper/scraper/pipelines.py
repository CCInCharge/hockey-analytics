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