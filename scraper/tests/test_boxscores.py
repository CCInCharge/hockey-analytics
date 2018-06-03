import unittest
from scraper.tests.responses import fake_response_from_file
from scraper.scraper.spiders import boxscores

class BoxscoresSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = boxscores.BoxscoresSpider()

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('boxscore_fake_response.html'))