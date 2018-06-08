import unittest
from scraper.tests.responses import fake_response_from_file
from scraper.scraper.spiders import team_abbrv

class TeamAbbrvSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = team_abbrv.TeamAbbrvSpider()
        self.response = fake_response_from_file('abbrv_fake_response.html')
        self.eastern = self.response.css("#standings_EAS tbody .full_table th a")
        self.western = self.response.css("#standings_WES tbody .full_table th a")

    def test_parse_data_from_link(self):
        link = self.western[0]
        data = self.spider._TeamAbbrvSpider__parse_data_from_link(link)
        self.assertEqual(data["abbrv"], "STL")
        self.assertEqual(data["year"], 2000)
        self.assertEqual(data["name"], "St. Louis Blues")
    
    def test_parse_data_from_link(self):
        link = self.eastern[10]
        data = self.spider._TeamAbbrvSpider__parse_data_from_link(link)
        self.assertEqual(data["abbrv"], "WSH")
        self.assertEqual(data["year"], 2000)
        self.assertEqual(data["name"], "Washington Capitals")