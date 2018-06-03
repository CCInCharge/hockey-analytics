import unittest
from scraper.tests.responses import fake_response_from_file
from scraper.scraper.spiders import hockey_reference

class HockeyReferenceSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = hockey_reference.HockeyReferenceSpider()
        self.response = fake_response_from_file('hockey_reference_fake_response.html')
        self.reg_season_table = self.response.css('#all_games #games tbody tr')
        self.playoffs_table = self.response.css('#all_games_playoffs #games_playoffs '
            'tbody tr')
    
    def test_parse_data_from_row(self):
        game = self.spider \
            ._HockeyReferenceSpider__parse_data_from_row(self \
            .reg_season_table[0])
        self.assertEqual(game["date_string"], "2016-10-12")
        self.assertIn("201610120CHI.html", game["game_link"])
        self.assertEqual(game["visitor_team"], "St. Louis Blues")
        self.assertEqual(game["visitor_goals"], 5)
        self.assertEqual(game["home_team"], "Chicago Blackhawks")
        self.assertEqual(game["home_goals"], 2)
    
    def test_parse_data_from_row_2(self):
        game = self.spider \
            ._HockeyReferenceSpider__parse_data_from_row(self \
            .reg_season_table[3])
        self.assertEqual(game["date_string"], "2016-10-12")
        self.assertIn("201610120SJS.html", game["game_link"])
        self.assertEqual(game["visitor_team"], "Los Angeles Kings")
        self.assertEqual(game["visitor_goals"], 1)
        self.assertEqual(game["home_team"], "San Jose Sharks")
        self.assertEqual(game["home_goals"], 2)