from selenium import webdriver
from pandas.io.html import read_html
import time
import pandas as pd
import numpy as np
import pickle


# whoscored.com selenium crawling code
def defence (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('/Users/riversong/Desktop/Fastcampus/Coding/crawling/chromedriver')
    driver.get(url)
    driver.set_window_size(3000,3000)

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

    driver.quit()
    return(df_defensive)
def attack (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('/Users/riversong/Desktop/Fastcampus/Coding/crawling/chromedriver')
    driver.get(url)
    driver.set_window_size(1500,3000)

    # click 'Offensive' button
    time.sleep(sleep_time)
    offence = driver.find_element_by_link_text('Offensive')
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

    driver.quit()
    return(df_offensive)
def midfield (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('/Users/riversong/Desktop/Fastcampus/Coding/crawling/chromedriver')
    driver.get(url)
    driver.set_window_size(3000,3000)

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

    driver.quit()
    return(df_passing)
def summary (url, sleep_time) :
    #open webdriver
    driver = webdriver.Chrome('/Users/riversong/Desktop/Fastcampus/Coding/crawling/chromedriver')
    driver.get(url)
    driver.set_window_size(3000,3000)

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
    
    driver.quit()
    return(df_summary) 