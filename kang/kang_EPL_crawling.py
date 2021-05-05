from selenium import webdriver
from pandas.io.html import read_html
import time
import pandas as pd
import numpy as np

def defensive (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('/Users/riversong/Desktop/Fastcampus/Coding/crawling/chromedriver')
    driver.get(url)

    #click 'accept' button
    time.sleep(sleep_time)
    # accept = driver.find_element_by_css_selector('#qcCmpButtons > button:nth-child(2)')
    # accept.click()

    #click 'defensive' button
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

url = 'https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/8228/Stages/18685/PlayerStatistics/England-Premier-League-2020-2021'
df = defensive(url, 5)
