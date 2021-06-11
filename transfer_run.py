import pickle
from crawl_transfer import *

leagues_name = ["premier", "laliga", "bundesliga", "serie_a", "ligue_1]
leagues_5= [
    {"league_1": "premier-league", "league_2": "GB1"},
    {"league_1": "primera-division", "league_2": "ES1"},
    {"league_1": "1-bundesliga", "league_2": "L1"},
    {"league_1": "serie-a", "league_2": "IT1"},
    {"league_1": "ligue-1", "league_2": "FR1"}
]


for idx in range(len(leagues_5)):
    crawl_links = crawl_player_links(**leagues_5[idx])
    df = crawl_transfer_stats(crawl_links)

    with open(f'datas/{leagues_name[idx]}.pkl', 'wb') as f:
        pickle.dump(df, f)

print("End Crawling")