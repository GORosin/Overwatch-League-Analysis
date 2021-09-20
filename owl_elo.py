import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
import random
from sklearn.utils import shuffle
import csv
import datetime

update_config = 0
elo_reduction = 0
team_map_diff = {"PHI": 0, "LDN": 0, "BOS": 0, "NYE": 0, "PAR": 0, "GLA": 0,
                 "SHD": 0, "DAL": 0, "CDH": 0, "VAL": 0, "SEO": 0, "HZS": 0,
                 "GZC": 0, "TOR": 0, "WAS": 0, "HOU": 0, "ATL": 0, "FLA": 0,
                 "SFS": 0, "VAN": 0}


def update_scores(teamA, teamB, scoreA, scoreB, teams, update):
    QA = 10 ** (teams[teamA] / 400)
    QB = 10 ** (teams[teamB] / 400)
    QA, QB = (QA + elo_reduction * QB) / (1 + elo_reduction), (QB + elo_reduction * QA) / (1 + elo_reduction)

    ExpectedA = QA / (QA + QB)
    ExpectedB = QB / (QA + QB)
    # so two ways to calculate scores, either normalize them
    # normA=scoreA/(scoreA+scoreB)
    # normB=scoreB/(scoreA+scoreB)
    # or 1 for win 0 for loss 0.5 for draw
    if scoreA == scoreB:
        normA, normB = 0.5, 0.5
    else:
        normA = 1 if scoreA > scoreB else 0
        normB = 1 if scoreA < scoreB else 0
    teams[teamA] += update * (normA - ExpectedA)
    teams[teamB] += update * (normB - ExpectedB)


def loop_maps(data):
    teams = {"Philadelphia Fusion": 1000, "London Spitfire": 1000, "Boston Uprising": 1000,
             "New York Excelsior": 1000, "Paris Eternal": 1000, "Los Angeles Gladiators": 1000,
             "Shanghai Dragons": 1000, "Dallas Fuel": 1000, "Chengdu Hunters": 1000,
             "Los Angeles Valiant": 1000, "Seoul Dynasty": 1000, "Hangzhou Spark": 1000,
             "Guangzhou Charge": 1000, "Toronto Defiant": 1000, "Washington Justice": 1000,
             "Houston Outlaws": 1000, "Atlanta Reign": 1000, "Florida Mayhem": 1000,
             "San Francisco Shock": 1000, "Vancouver Titans": 1000}
    for index, row in data.iterrows():
        stage = int(row["stage"])
        update = stage * 10
        if row['map_winner'] == 'draw':
            update_scores(row['team_one_name'], row['team_two_name'],
                          row['winning_team_final_map_score'], row['losing_team_final_map_score'], teams, update)
        else:
            update_scores(row["map_winner"], row["map_loser"],
                          row['winning_team_final_map_score'], row['losing_team_final_map_score'], teams, update)
    rounded_dict = {key: round(value, 1) for key, value in teams.items()}
    sorted_dict = sorted(rounded_dict.items(), key=lambda x: x[1])

    print(sorted_dict)


def loop_series(series, teams):
    teamA, teamB = series[0:2]
    for i in range(2, 9, 2):
        scoreA, scoreB = series[i:i + 2]
        update_scores(teamA, teamB, scoreA, scoreB, teams, update_config)
    if not (series[10] == series[11]):
        update_scores(teamA, teamB, series[10], series[11], teams, update=update_config)


def loop_matches(owl_data, teams):
    for series in owl_data.values:
        loop_series(series, teams)
    return


def rank_teams(iterations, update, stage="stage3", elo_coeff=0):
    teams = {"PHI": 1000, "LDN": 1000, "BOS": 1000, "NYE": 1000, "PAR": 1000, "GLA": 1000,
             "SHD": 1000, "DAL": 1000, "CDH": 1000, "VAL": 1000, "SEO": 1000, "HZS": 1000,
             "GZC": 1000, "TOR": 1000, "WAS": 1000, "HOU": 1000, "ATL": 1000, "FLA": 1000,
             "SFS": 1000, "VAN": 1000}
    global elo_reduction
    elo_reduction = elo_coeff
    global update_config
    update_config = update
    owl_data = pd.read_csv(str(stage) + ".csv")
    # owl_data=shuffle(owl_data)
    # plot out how a team looks after every match

    # number of iterations

    for i in range(iterations):
        loop_matches(owl_data, teams)

    # plt.plot(range(len(my_team)),my_team)
    # plt.show()
    # rankings= sorted(teams.items(), key=operator.itemgetter(1))

    # return rankings
    return teams


def inter_stage_ranking(iterations, update):
    stage_1 = rank_teams(10, update, "stage1")
    stage_2 = rank_teams(iterations, update, "stage2")
    stage_3 = rank_teams(10, update, "stage3")
    team_rankings = {}
    for k, v in stage_1.items():
        team_rankings[k] = 0.2 * stage_1[k] + 0.8 * stage_2[k]

    rankings = sorted(team_rankings.items(), key=operator.itemgetter(1))
    return rankings


def read_csv(csv_file):
    # column 3 = match id, 4 = game, 6 = map winner, 7 = map loser,
    # 8 = map name, 10 = winner score, 11 = loser score
    match_id = 0
    game_num = 0
    maps = pd.read_csv(csv_file)
    maps = maps.loc[:, maps.columns.intersection(['round_start_time',
                                                  'match_id', 'game_number',
                                                  'map_name', 'map_winner', 'map_loser',
                                                  'winning_team_final_map_score',
                                                  'losing_team_final_map_score',
                                                  'team_one_name', 'team_two_name'])]
    maps['stage'] = np.nan
    for index, line in maps.iterrows():
        if line['match_id'] == match_id and line['game_number'] == game_num:
            maps.drop(index, inplace=True)
        else:
            match_id = line['match_id']
            game_num = line['game_number']
            year = int(line['round_start_time'][0:4])
            month = int(line['round_start_time'][5:7])
            day = int(line['round_start_time'][8:10])
            date = datetime.datetime(year, month, day)
            if date < datetime.datetime(2021, 5, 20):
                maps.at[index, 'stage'] = 1
            elif datetime.datetime(2021, 5, 20) < date < datetime.datetime(2021, 6, 26):
                maps.at[index, 'stage'] = 2
            elif datetime.datetime(2021, 6, 24) < date < datetime.datetime(2021, 7, 29):
                maps.at[index, 'stage'] = 3
            elif datetime.datetime(2021, 7, 29) < date < datetime.datetime(2021, 9, 4):
                maps.at[index, 'stage'] = 4
            else:
                maps.at[index, 'stage'] = 5
    maps.drop(['round_start_time', 'match_id', 'game_number'], axis=1, inplace=True)
    return maps


if __name__ == "__main__":
    """
    rankings = inter_stage_ranking(20, 5)
    for i in rankings[::-1]:
        print("team:" + str(i[0]) + " elo:" + str(int(i[1])))
    """
    loop_maps(read_csv("match_map_stats.csv"))
