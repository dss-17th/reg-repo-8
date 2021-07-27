Champions = ['Manchester City', 'Liverpool FC', 'Chelsea FC','Manchester United','FC Barcelona', 'Atlético Madrid',
       'Real Madrid','Sevilla FC','Bayern Munich', 'Borussia Dortmund','RB Leipzig','VfL Wolfsburg',
            'Juventus FC', 'Inter Milan', 'AC Milan', 'Atalanta BC','LOSC Lille','Paris Saint-Germain', 'AS Monaco']
Europa = ['Leicester City','West Ham United','Real Sociedad', 'Villarreal CF','Real Betis Balompié', 
         'Eintracht Frankfurt','Bayer 04 Leverkusen','1.FC Union Berlin','SSC Napoli','AS Roma','SS Lazio',
         'Olympique Lyon']
Relegation = ['Fulham FC','West Bromwich Albion','Sheffield United','SD Eibar', 'Real Valladolid CF', 'SD Huesca',
             'SV Werder Bremen','FC Schalke 04','Benevento Calcio','FC Crotone','Parma Calcio 1913',
             'Dijon FCO', 'Nîmes Olympique']

def convert_club(club):
    if club in Champions:
        score = 3
    elif club in Europa:
        score = 2
    elif club in Relegation:
        score = 0
    else:
        score = 1
    
    return score


def preprocess_df(df):
    df.drop(columns=['sns', 'cluster'], inplace=True)
    df = df.astype({col: "int" for col in ["market_value", "app", "age", "height"]})
    df.reset_index(drop=True, inplace=True)

    df['club'] = df['club'].apply(convert_club)
    df['position'] = df['position'].apply(lambda x: "-".join(x.split("-")[1:]))
    
    df.columns = ['market_value', 'app', 'conceded_goals', 'clean_sheets', 'yellow_card',
       'second_yell', 'red_card', 'age', 'height', 'position', 'foot', 'club',
       'outfitter', 'cup', 'Tackles', 'Inter', 'Fouls', 'Offsides', 'Clear',
       'Drbed', 'Blocks', 'OwnG', 'Rating', 'Goals', 'Assists', 'SpG', 'KeyP_2',
       'Fouled', 'Off', 'Disp', 'UnsTch', 'Drb', 'KeyP', 'AvgP', 'PS',
       'Crosses', 'LongB', 'ThrB', 'AerialsWon', 'MotM', 'period']

    df.drop('KeyP_2', 1, inplace=True)
    
    others_ls = list(set(df['outfitter'].unique()) - {'Nike', 'adidas', 'Puma'})
    others = {col: 'others' for col in others_ls}

    df['outfitter'] =  df['outfitter'].replace(others)
    
    df['total_out'] = df['second_yell'] + df['red_card']
    
    return df