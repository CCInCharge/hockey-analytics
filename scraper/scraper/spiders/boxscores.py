# -*- coding: utf-8 -*-
import scrapy


class BoxscoresSpider(scrapy.Spider):
    name = 'boxscores'
    allowed_domains = ['https://www.hockey-reference.com/boxscores']
    download_delay = 3

    def __get_period_rows(self, rows):
        """
        Given a scrapy.SelectorList of rows from the scoring summary table,
        returns the indices of the table rows which denote the period in which
        a goal is scored.

        :param rows: scrapy.SelectorList of rows from scoring summary table
        :returns: dict, with keys representing each period and values
        representing the index of the SelectorList in which this occurs
        """
        score_indices = {"OT_periods": 0, "header_rows": []}
        for i in range(len(rows)):
            row_text = rows[i].css("::text").extract_first()
            if row_text == "1st Period":
                score_indices["1st"] = i
                score_indices["header_rows"].append(i)
            elif row_text == "2nd Period":
                score_indices["2nd"] = i
                score_indices["header_rows"].append(i)
            elif row_text == "3rd Period":
                score_indices["3rd"] = i
                score_indices["header_rows"].append(i)
            elif "OT" in row_text:
                score_indices["OT"] = i
                score_indices["header_rows"].append(i)
                # Assumes there are never more than 9 OT periods
                score_indices["OT_periods"] = int(row_text[0])
            elif row_text == "Shootout":
                score_indices["SO"] = i
                score_indices["header_rows"].append(i)
                score_indices["OT_periods"] = 1
        return score_indices
    
    def __get_goal_data(self, row, row_ind, score_indices):
        goal_period = ""
        row_text = row.css("td::text").extract()
        if score_indices.get("SO", None) and row_ind > score_indices["SO"]:
            goal_period = "SO"
        elif score_indices.get("OT", None) and row_ind > score_indices["OT"]:
            goal_period = str(score_indices["OT_periods"]) + "OT"
        elif score_indices.get("3rd", None) and row_ind > score_indices["3rd"]:
            goal_period = "3rd"
        elif score_indices.get("2nd", None) and row_ind > score_indices["2nd"]:
            goal_period = "2nd"
        elif score_indices.get("1st", None) and row_ind > score_indices["1st"]:
            goal_period = "1st"
        if goal_period is not "SO":
            raw_time_text = row_text[0]
            time_minutes = int(raw_time_text[0:2])
            time_seconds = int(raw_time_text[3:5])
            team_abrv = row.css("td")[1].css("a::text")[0].extract()
            if "OT" in goal_period:
                time_minutes += (60 + (score_indices["OT_periods"] - 1) * 20)
            else:
                time_minutes += (20 * (int(goal_period[0]) - 1))
            
            # Determine if the goal is even strength or special (PP, SH, etc)
            to_remove = ['\n', '\t', '\xa0', ' ', '-', '—']
            special = row_text[1]
            for char in to_remove:
                special = special.replace(char, '')
            if 'PP' in special or 'SH' in special or 'EN' in special:
                specials = special.split('')
            else:
                specials = []

    def parse(self, response):
        rows = response.css("#scoring tr")
        # TODO: Need to only loop through data rows, non-header rows
        score_indices = self.__get_period_rows(rows)

