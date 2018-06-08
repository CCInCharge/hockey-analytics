# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
import configparser

class TeamAbbrvPipeline(object):
    def open_spider(self, spider):
        config = configparser.ConfigParser()
        config.read('config/db_config.cfg')
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
        # TODO: Save to DB
        
        return item