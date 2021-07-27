import time
import pickle
import numpy as np
import pandas as pd
import urllib.parse
import requests
from bs4 import BeautifulSoup
from scrapy.http import TextResponse
from fake_useragent import UserAgent


def crawl_player_links(league_1, league_2):
    url = f"https://www.transfermarkt.co.uk/{league_1}/startseite/wettbewerb/{league_2}"
    headers = {"User-Agent": UserAgent().Chrome}

    # 리그 url 접속 : scrapy
    req = requests.get(url, headers=headers)
    response_1 = TextResponse(req.url, body=req.text, encoding="utf-8")

    # club link 수집
    links = response_1.xpath('//*[@id="yw1"]/table/tbody/tr/td[1]/a/@href').extract()
    links = [response_1.urljoin(link) for link in links]

    # 각 club 마다 선수 link 수집 : bs4
    player_links = []
    for link in links:
        time.sleep(3)
        req = requests.get(link, headers=headers)
        response = BeautifulSoup(req.content, 'html.parser')
        
        elements = response.select("#yw1 > table > tbody > tr")
        for element in elements:
            player_link = response_1.urljoin(element.select('a')[-1].get('href'))
            player_links.append(player_link)

    return player_links


def crawl_transfer_stats(player_links):

    # dataframe 스키마 생성
    cols = ['name', 'market_value', 'app', 'conceded_goals', 'clean_sheets',
            'yellow_card', 'second_yell', 'red_card', 'age', 'height', 'position',
            'foot', 'club', 'joined', 'expire', 'last_contract', 'outfitter','sns', 'cup']
    df = pd.DataFrame(columns=cols)

    # 해당 리그의 각 선수 상세페이지 url request
    for detail_link in tqdm(player_links):
        time.sleep(1.5)
        req = requests.get(detail_link, headers=headers)
        response = BeautifulSoup(req.content, 'html.parser')

        # 이름과 현재가치 
        try:
            name = response.select('#main > div:nth-child(12) > div > div > div.dataMain > div > div.dataName > h1')[0].text
            market_value = response.select('#main > div:nth-child(12) > div > div > div.dataMarktwert > a')[0].text.split(" ")[0]
        except:
            continue

        # cup
        try:
            elements = response.select('div.dataErfolge > a.dataErfolg')
            
            cup = 0
            for element in elements:
                cup += int(element.select_one('span').text)
        except:
            cup = np.NaN

        # 경기스텟
        try:
            app = response.find_all('span', 'wert')[0].text
            yellow_card = response.find_all('span', 'wert')[1].text
            conceded_goals = response.find_all('span', 'wert')[2].text
            second_yell = response.find_all('span', 'wert')[3].text
            clean_sheets = response.find_all('span', 'wert')[4].text
            red_card = response.find_all('span', 'wert')[5].text
        except:
            app = conceded_goals = clean_sheets = yellow_card = second_yell = red_card = None

        # 선수 information
        for info in response.find_all('tr')[:15]:
            if info.find('th') is None:
                continue
            
            if info.find('th').text.strip()[:-1] == "Age":
                age = info.find('td').text
            elif info.find('th').text[:-1] == "Height":
                height = info.find('td').text.replace("\xa0m", "")
            elif info.find('th').text[:-1] == "Position":
                position = info.find('td').text.replace(" ", "").replace("\n", "")
            elif info.find('th').text[:-1] == "Foot":
                foot = info.find('td').text
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

        # outfitter
        try:
            outfitter
        except:
            outfitter = None

        # 크롤링정보를 list의 dictionary형태로 dataframe 생성
        data = {
            'name': name, 'market_value': market_value, 'app': app, 'conceded_goals': conceded_goals,
            'clean_sheets': clean_sheets, 'yellow_card': yellow_card, 'second_yell': second_yell,
            'red_card': red_card, 'age': age, 'height': height, 'position': position, 'foot': foot,
            'club': club, 'joined': joined, 'expire': expire, 'last_contract': last_contract,
            'outfitter': outfitter, 'sns': sns, 'cup': cup
        }
        df.loc[len(df)] = data

    return df