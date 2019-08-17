class Whoscored:
    
    def __init__(self, url='https://www.whoscored.com/Regions/252/Tournaments/7/England-Championship'):            
        self.url = url
        self.team_urls = None
        self.league_table = None
        self.team_info = None
        
    def get_league_table(self):

        league_table = []

        driver = webdriver.Chrome()
        driver.get(self.url)

        links = driver.find_elements_by_css_selector("#standings-16389-content tr")

        for link in links:
            rank = link.find_element_by_css_selector(".o").text
            team = link.find_element_by_css_selector(".team").text
            played = link.find_element_by_css_selector(".p").text
            win = link.find_element_by_css_selector(".w").text
            draw = link.find_element_by_css_selector(".d").text
            loss = link.find_element_by_css_selector(".l").text
            goal_for = link.find_element_by_css_selector(".gf").text
            goal_against = link.find_element_by_css_selector(".ga").text
            goal_difference = link.find_element_by_css_selector(".gd").text
            points = link.find_element_by_css_selector(".pts").text

            table_data = {
                "rank" : rank,
                "team" : team,
                "played" : played,
                "win" : win,
                "draw" : draw,
                "loss" : loss,
                "goal_for" : goal_for,
                "goal_against" : goal_against,
                "goal_difference" : goal_difference,
                "points" : points,
            }

            league_table.append(table_data)

        driver.quit()

        return league_table 
    
    def get_team_url(self):

        team_urls = []

        driver = webdriver.Chrome()
        driver.get(self.url)

        links = driver.find_elements_by_css_selector("#standings-16389-content tr")

        for link in links:
            url_link = link.find_element_by_css_selector("td:nth-child(2) > a").get_attribute("href")
            team_urls.append(url_link)

        driver.quit()

        return team_urls
    
    def get_team_information(self):

        team_info = []

        for team_url in self.team_urls:

            driver = webdriver.Chrome()
            driver.get(team_url)

            items = driver.find_elements_by_css_selector(".stats-container > .stats > dd")

            datas = []

            for idx, item in enumerate(items):
                if idx == 8:
                    datas.append(item.find_element_by_css_selector(".yellow-card-box").text)
                    datas.append(item.find_element_by_css_selector(".red-card-box").text)
                else : 
                    datas.append(item.text)

            data = {
                "goals_per_game" : datas[2],
                "avg_possession" : datas[3],
                "pass_accuracy" : datas[4],
                "shots_per_game" : datas[5],
                "tackles_per_game" : datas[6],
                "dribbles_per_game" : datas[7],
                "yellow_card" : datas[8],
                "red_card" : datas[9],
            }

            team_info.append(data)
            driver.quit()

        return team_info    
    
    def making_df(self):

        result = []

        for count in range(0,23+1):

            data = dict(self.league_table[count], **self.team_info[count])

            result.append(data)

        df = pd.DataFrame(result)

        df = df[[
            "team",
            "rank",
            "points",
            "played",
            "win",
            "draw",
            "loss",
            "goal_for",
            "goal_against",
            "goal_difference",
            "goals_per_game",
            "avg_possession",
            "pass_accuracy",
            "shots_per_game",
            "tackles_per_game",
            "dribbles_per_game",
            "yellow_card",
            "red_card",
        ]]


        return df

    def crawling(self):
        self.team_urls = self.get_team_url()
        self.league_table = self.get_league_table()
        self.team_info = self.get_team_information()
        result = self.making_df()

        return result
    
    
whoscored = Whoscored()
df = whoscored.crawling()
df.to_csv(index=False)