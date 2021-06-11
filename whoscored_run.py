from Library.whoscored_crawling import *
# 수집하고자 하는 5대리그의 데이터 주소
urls = [
    'https://1xbet.whoscored.com/Regions/206/Tournaments/4/Seasons/8321/Stages/18851/PlayerStatistics/Spain-LaLiga-2020-2021',
    'https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/8228/Stages/18685/PlayerStatistics/England-Premier-League-2020-2021',
    'https://1xbet.whoscored.com/Regions/108/Tournaments/5/Seasons/8330/Stages/18873/PlayerStatistics/Italy-Serie-A-2020-2021',
    'https://1xbet.whoscored.com/Regions/81/Tournaments/3/Seasons/8279/Stages/18762/PlayerStatistics/Germany-Bundesliga-2020-2021',
    'https://1xbet.whoscored.com/Regions/74/Tournaments/22/Seasons/8185/Stages/18594/PlayerStatistics/France-Ligue-1-2020-2021'
]
# 셀레니움 실행코드
for url in urls:
    defence_df = defence(url, 2)
    attack_df = attack(url, 2)
    midfield_df = midfield(url, 2)
    summary_df = summary(url, 2)
    league = pd.merge(pd.merg(defence_df,attack_df,on='Player.1'),\
                      pd.merge(midfield_df,summary_df,on='Player.1'),on='Player.1')
    total = pd.concat([total,league], axis=0)
    league = pd.DataFrame()

# 데이터 저장하기
with open('datas/all_league.pkl', 'wb') as f:
    pickle.dump(total, f)