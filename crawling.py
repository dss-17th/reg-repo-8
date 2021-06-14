from selenium import webdriver
from pandas.io.html import read_html
import time
import pandas as pd
import numpy as np

# whoscored.com selenium crawling code

def defence (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('#chrome driver')
    driver.get(url)

    # click 'defensive' button
    time.sleep(sleep_time)
    defense = driver.find_element_by_link_text('Defensive')
    defense.click()

    #click 'all players' button
    time.sleep(sleep_time)
    all_player = driver.find_element_by_link_text('All players')
    all_player.click()

    #get the total page number
    time.sleep(sleep_time)
    page = driver.find_element_by_link_text('last')
    total_page = int(page.get_attribute('data-page'))

    #create the dataframe
    df_defensive = pd.DataFrame(columns = ['Player', 'Player.1', 'Apps', 'Mins', 'Tackles', 'Inter', 'Fouls',
       'Offsides', 'Clear', 'Drb', 'Blocks', 'OwnG', 'Rating'])

    #crawling the table
    for i in np.arange(total_page) :
        time.sleep(sleep_time)
        table = driver.find_element_by_xpath('//*[@id="statistics-table-defensive"]')
        table_html= table.get_attribute('innerHTML')
        df2 = read_html(table_html)[0]
        df_defensive = pd.concat([df_defensive, df2], axis=0)
        driver.find_element_by_link_text('next').click()

    return(df_defensive)
def attack (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('#chrome driver')
    driver.get(url)

    # click 'Offensive' button
    time.sleep(sleep_time)
    defense = driver.find_element_by_link_text('Offensive')
    offence.click()

    #click 'all players' button
    time.sleep(sleep_time)
    all_player = driver.find_element_by_link_text('All players')
    all_player.click()

    #get the total page number
    time.sleep(sleep_time)
    page = driver.find_element_by_link_text('last')
    total_page = int(page.get_attribute('data-page'))

    #create the dataframe
    df_offensive = pd.DataFrame(columns = ['Player', 'Player.1', 'Apps', 'Mins', 'Tackles', 'Inter', 'Fouls',
       'Goals', 'Assists', 'SpG', 'KeyP', 'Fouled', 'Off','Disp','UnsTch','Rating'])

    #crawling the table
    for i in np.arange(total_page) :
        time.sleep(sleep_time)
        table = driver.find_element_by_xpath('//*[@id="statistics-table-offensive"]')
        table_html= table.get_attribute('innerHTML')
        df2 = read_html(table_html)[0]
        df_offensive = pd.concat([df_offensive, df2], axis=0)
        driver.find_element_by_link_text('next').click()

    return(df_offensive)
def midfield (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('#chrome driver')
    driver.get(url)

    # click 'defensive' button
    time.sleep(sleep_time)
    passing = driver.find_element_by_link_text('Passing')
    passing.click()

    #click 'all players' button
    time.sleep(sleep_time)
    all_player = driver.find_element_by_link_text('All players')
    all_player.click()

    #get the total page number
    time.sleep(sleep_time)
    page = driver.find_element_by_link_text('last')
    total_page = int(page.get_attribute('data-page'))

    #create the dataframe
    df_passing = pd.DataFrame(columns = ['Player', 'Player.1', 'Apps', 'Mins', 'Tackles', 'Inter', 'Fouls',
       'Assists', 'KeyP', 'AvgP', 'PS%', 'Crosses', 'LongB','ThrB','Rating'])

    #crawling the table
    for i in np.arange(total_page) :
        time.sleep(sleep_time)
        table = driver.find_element_by_xpath('//*[@id="stage-top-player-stats-passing"]')
        table_html= table.get_attribute('innerHTML')
        df2 = read_html(table_html)[0]
        df_passing = pd.concat([df_passing, df2], axis=0)
        driver.find_element_by_link_text('next').click()

    return(df_passing)
def summary (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('#chrome driver')
    driver.get(url)

    #click 'all players' button
    time.sleep(sleep_time)
    all_player = driver.find_element_by_link_text('All players')
    all_player.click()

    #get the total page number
    time.sleep(sleep_time)
    page = driver.find_element_by_link_text('last')
    total_page = int(page.get_attribute('data-page'))

    #create the dataframe
    df_summary = pd.DataFrame(columns = ['Player', 'Player.1', 'Apps', 'Mins', 'Goals', 'Assists', 'Yel',
       'Red', 'SpG', 'PS%', 'AerialsWon', 'MotM', 'Rating'])

    #crawling the table
    for i in np.arange(total_page) :
        time.sleep(sleep_time)
        table = driver.find_element_by_xpath('//*[@id="stage-top-player-stats-summary"]')
        table_html= table.get_attribute('innerHTML')
        df2 = read_html(table_html)[0]
        df_summary = pd.concat([df_summary, df2], axis=0)
        driver.find_element_by_link_text('next').click()

    return(df_summary)

url = 'https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/8228/Stages/18685/PlayerStatistics/England-Premier-League-2020-2021'
defence_df = defence(url, 5)
attack_df = attack(url, 5)
midfield_df = midfield(url, 5)
summary_df = summary(url, 5)

# transfermarkt.com crawling code
cols = ['name', 'market_value', 'app', 'conceded_goals', 'clean_sheets',
        'yellow_card', 'second_yell', 'red_card', 'age', 'height', 'citizenship',
        'position', 'foot', 'agent', 'club', 'joined', 'expire', 'last_contract',
        'outfitter','sns','caps_goals']

df = pd.DataFrame(columns=cols)

league, order = "premier-league", "GB1"
base_url = f"https://www.transfermarkt.co.uk/{league}/startseite/wettbewerb/{order}"

headers = {'User-Agent': UserAgent().chrome}
response = requests.get(base_url, headers=headers)
dom = BeautifulSoup(response.content, "html.parser")

# 리그별 클럽의 링크데이터
elements = dom.select("#yw1 > table > tbody > tr")

base_link = "https://www.transfermarkt.co.uk"
links = []
for element in elements:
    link = element.select_one("a").get("href")
    link = urllib.parse.urljoin(base=base_link, url=link, allow_fragments=True)
    links.append(link)

for link in links:
    response = requests.get(link, headers=headers)
    dom = BeautifulSoup(response.content, "html.parser")

    # 리그의 선수 링크데이터
    elements = dom.select("#yw1 > table > tbody > tr")

    player_links = []
    for element in elements:
        player_link = element.select('a')[-1].get('href')
        player_link = urllib.parse.urljoin(base=base_link, url=player_link, allow_fragments=True)
        player_links.append(player_link)

        # 선수별 정보데이터
    for player_link in player_links:
        headers = {'User-Agent': UserAgent().chrome}
        response = requests.get(player_link, headers=headers)
        dom = BeautifulSoup(response.content, 'html.parser')

        name = dom.select_one('#main > div:nth-child(12) > div > div > div.dataMain > div > div.dataName > h1').text
        print(name)
        try:
            vals = dom.select('#main > div:nth-child(12) > div > div > div.dataContent > div > div:nth-child(3) > p.hide-for-small.notTablet > span.dataValue > a')
            caps_goals = int(vals[0].text) / int(vals[1].text)
        except:
            caps_goals = None
        try:
            market_value = dom.select_one('#main > div:nth-child(17) > div.large-8.columns > div:nth-child(2) > div.row.collapse > div.large-6.large-push-6.small-12.columns > div > div.box.viewport-tracking > div.row.collapse > div > div > div > div.row.collapse > div.large-5.columns.small-12 > div > div.zeile-oben > div.right-td > a:nth-child(1)').text
        except:
            market_value = None
        try:
            app = dom.find_all('span', 'wert')[0].text
            conceded_goals = dom.find_all('span', 'wert')[2].text
            clean_sheets = dom.find_all('span', 'wert')[4].text
            yellow_card = dom.find_all('span', 'wert')[1].text
            second_yell = dom.find_all('span', 'wert')[3].text
            red_card = dom.find_all('span', 'wert')[5].text
        except:
            app, conceded_goals, clean_sheets, yellow_card, second_yell, red_card = None, None, None, None, None, None

        for info in dom.find_all('tr')[:15]:
            if info.find('th') is None:
                continue

            if info.find('th').text.strip()[:-1] == "Age":
                age = info.find('td').text
            elif info.find('th').text[:-1] == "Height":
                height = info.find('td').text
            elif info.find('th').text[:-1] == "Citizenship":
                citizenship = len(np.unique(info.find('td').text))
            elif info.find('th').text[:-1] == "Position":
                position = info.find('td').text.replace(" ", "").replace("\n", "")
            elif info.find('th').text[:-1] == "Foot":
                foot = info.find('td').text
            elif info.find('th').text[:-1] == "Player agent":
                agent = info.find('td').text.replace("\n", "")
            elif info.find('th').text.strip()[:-1] == "Current club":
                club = info.find('td').text.strip()
            elif info.find('th').text.strip()[:-1] == "Joined":
                joined = info.find('td').text.strip()
            elif info.find('th').text.strip()[:-1] == "Contract expires":
                expire = info.find('td').text.strip()
            elif info.find('th').text.strip()[:-1] == "Date of last contract extension":
                last_contract = info.find('td').text.strip()
            elif info.find('th').text.strip()[:-1] == "Outfitter":
                outfitter = info.find('td').text.strip()
            elif info.find('th').text.strip()[:-1] == "Social-Media":
                sns = len(info.find_all('a'))

        data = {
            'name': name, 'market_value': market_value, 'caps_goals': caps_goals, 'app': app,
            'conceded_goals': conceded_goals,
            'clean_sheets': clean_sheets, 'yellow_card': yellow_card, 'second_yell': second_yell,
            'red_card': red_card, 'age': age, 'height': height, 'citizenship': citizenship,
            'position': position, 'foot': foot, 'agent': agent, 'club': club, 'joined': joined,
            'expire': expire, 'last_contract': last_contract, 'outfitter': outfitter, 'sns': sns
        }

        df.loc[len(df)] = data
        time.sleep(0.5)
