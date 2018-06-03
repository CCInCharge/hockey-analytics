import unittest
from scraper.tests.responses import fake_response_from_file
from scraper.scraper.spiders import boxscores

class BoxscoresSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = boxscores.BoxscoresSpider()
        self.response = fake_response_from_file('boxscore_fake_response.html')
        self.rows = self.response.css("#scoring tr")
        self.score_indices = self.spider._BoxscoresSpider__get_period_rows(self.rows)

    def test_score_indices(self):
        self.assertEqual(self.score_indices['1st'], 0)
        self.assertIsNone(self.score_indices.get('2nd', None))
        self.assertEqual(self.score_indices['3rd'], 3)
        self.assertIsNone(self.score_indices.get('OT', None))
        self.assertEqual(self.score_indices['OT_periods'], 1)
        self.assertEqual(self.score_indices['SO'], 6)
        self.assertEqual(self.score_indices['header_rows'], [0, 3, 6])
    
    def test_goal_1(self):
        goal = self.spider._BoxscoresSpider__get_goal_data(self.rows[1], 1,
            self.score_indices)
        self.assertEqual(goal["time_minutes"], 0)
        self.assertEqual(goal["time_seconds"], 24)
        self.assertEqual(goal["team_abrv"], 'LAK')
        self.assertEqual(goal["specials"], [])
    
    def test_goal_2(self):
        goal = self.spider._BoxscoresSpider__get_goal_data(self.rows[2], 2,
            self.score_indices)
        self.assertEqual(goal["time_minutes"], 6)
        self.assertEqual(goal["time_seconds"], 9)
        self.assertEqual(goal["team_abrv"], 'OTT')
        self.assertEqual(goal["specials"], [])

    def test_goal_3(self):
        goal = self.spider._BoxscoresSpider__get_goal_data(self.rows[4], 4,
            self.score_indices)
        self.assertEqual(goal["time_minutes"], 46)
        self.assertEqual(goal["time_seconds"], 36)
        self.assertEqual(goal["team_abrv"], 'OTT')
        self.assertEqual(goal["specials"], ['SH'])
    
    def test_shootout_goal(self):
        goal = self.spider._BoxscoresSpider__get_goal_data(self.rows[7], 7,
            self.score_indices)
        self.assertIsNone(goal)

class BoxscoresSpiderTest2(unittest.TestCase):
    def setUp(self):
        self.spider = boxscores.BoxscoresSpider()
        self.response = fake_response_from_file('boxscore_fake_response_2.html')
        self.rows = self.response.css("#scoring tr")
        self.score_indices = self.spider._BoxscoresSpider__get_period_rows(self.rows)

    def test_score_indices(self):
        self.assertIsNone(self.score_indices.get('1st', None))
        self.assertEqual(self.score_indices['2nd'], 0)
        self.assertEqual(self.score_indices['3rd'], 2)
        self.assertIsNone(self.score_indices.get('OT', None))
        self.assertEqual(self.score_indices['OT_periods'], 0)
        self.assertIsNone(self.score_indices.get('SO', None))
        self.assertEqual(self.score_indices['header_rows'], [0, 2])
    
    def test_goal_1(self):
        goal = self.spider._BoxscoresSpider__get_goal_data(self.rows[1], 1,
            self.score_indices)
        self.assertEqual(goal["time_minutes"], 24)
        self.assertEqual(goal["time_seconds"], 38)
        self.assertEqual(goal["team_abrv"], 'STL')
        self.assertEqual(goal["specials"], [])
    
    def test_goal_2(self):
        goal = self.spider._BoxscoresSpider__get_goal_data(self.rows[3], 3,
            self.score_indices)
        self.assertEqual(goal["time_minutes"], 45)
        self.assertEqual(goal["time_seconds"], 14)
        self.assertEqual(goal["team_abrv"], 'STL')
        self.assertEqual(goal["specials"], ['PP'])

    def test_goal_3(self):
        goal = self.spider._BoxscoresSpider__get_goal_data(self.rows[4], 4,
            self.score_indices)
        self.assertEqual(goal["time_minutes"], 57)
        self.assertEqual(goal["time_seconds"], 43)
        self.assertEqual(goal["team_abrv"], 'STL')
        self.assertEqual(goal["specials"], ['SH', 'EN'])