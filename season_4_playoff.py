from scipy.optimize import curve_fit
from math import exp
import numpy as np
import matplotlib.pyplot as plt
from random import random
import pandas as pd


def logistic(x, k=400):
    return 1 / (1 + np.exp(-1 * x / k))


team_elo = {"DAL": 988.5, "SHD": 1130.1, "GLA": 1261.4, "ATL": 1091, "CDH": 1229.5, "SFS": 1184.1, "WAS": 1053.8, "HOU": 980.1, "PHL": 1112.4,
            "TOR": 1012.3, "SEO": 1011.7, "PAR": 929.4, "BOS": 846.3, "HZS": 918.4, "FLR": 945.1, "NYXL": 1004.5, "GZC": 972.1, "LDN": 829.3,
            "VAN": 788.1, "LAV": 711.9}


def estimate_logistic():
    vs_dallas = {"ATL": 0.55, "BOS": 0.95, "FLR": 0.95, "GLA": 0.51, "LDN": 0.99, "PAR": 0.75, "SFS": 0.55, "TOR": 0.85,
                 "VAN": 0.99, "WAS": 0.6}

    vs_shanghai = {"CDH": 0.6, "GZC": 0.9, "HZS": 0.75, "LAV": 0.999, "NYXL": 0.7, "PHL": 0.55, "SEO": 0.65}

    d_xy = [(team_elo["DAL"] - team_elo[key], value, key) for key, value in vs_dallas.items()]
    sh_xy = [(team_elo["SHD"] - team_elo[key], value, key) for key, value in vs_shanghai.items()]
    xy_total = d_xy + sh_xy
    X = np.array([i[0] for i in xy_total] + [-1 * i[0] for i in xy_total])
    Y = np.array([i[1] for i in xy_total] + [1 - i[1] for i in xy_total])
    labels = [i[2] for i in xy_total] + [i[2] for i in xy_total]
    results, cov = curve_fit(logistic, X, Y)
    print(results)
    X_fit = np.linspace(-70, 70, 100)
    Y_fit1 = logistic(X_fit, 17.95)
    Y_fit2 = logistic(X_fit, 20)
    Y_fit3 = logistic(X_fit, 22)
    Y_fit4 = logistic(X_fit, 12)
    Y_fit5 = logistic(X_fit, 10)
    plt.plot(X_fit, Y_fit1)
    plt.plot(X_fit, Y_fit2)
    plt.plot(X_fit, Y_fit3)
    plt.plot(X_fit, Y_fit4)
    plt.plot(X_fit, Y_fit5)
    plt.plot(X, Y, ".")
    plt.ylabel("Probablity of team 1 winning")
    plt.xlabel("Power Ranking difference team 1 - team 2")
    # plt.savefig("elo_probality_estimate")
    for idx, (i, j) in enumerate(zip(X, Y)):
        plt.annotate(labels[idx], xy=(i, j), ha='center')
    plt.show()


class Results:
    def __init__(self, team1, team2, team_score1, team_score2):
        self.teams = (team1, team2)
        self.winner = self.teams[team_score1 < team_score2]
        self.loser = self.teams[team_score1 > team_score2]
        self.scores = (team_score1, team_score2)
    def __str__(self):
        return f"{self.teams[self.teams[0]<self.teams[1]]}-{self.teams[self.teams[0]>self.teams[1]]} {self.scores[self.teams[0]<self.teams[1]]} : {self.scores[self.teams[0]>self.teams[1]]} "

def match(team1, team2):
    score_team1 = 0
    score_team2 = 0
    team1_win_prob = logistic(team_elo[team1] - team_elo[team2])
    while score_team1 < 3 and score_team2 < 3:
        randnum=random()
        score_team1 += randnum < team1_win_prob
        score_team2 += randnum > team1_win_prob
    return Results(team1, team2, score_team1, score_team2)


def finals(team1, team2):
    score_team1 = 0
    score_team2 = 0
    team1_win_prob =logistic(team_elo[team1] - team_elo[team2])
    while score_team1 < 4 and score_team2 < 4:
        randnum=random()
        score_team1 += randnum < team1_win_prob
        score_team2 += randnum > team1_win_prob
    return Results(team1, team2, score_team1, score_team2)


def tournament_graph():
    # teams
    team1 = "SHD"
    team2 = "DAL"
    team3 = "CDH"
    team4 = "GLA"
    team5 = "ATL"
    team6 = "SFS"
    team7 = "PHL"
    team8 = "WAS"

    # Winners Bracket
    # first round
    match1_results = match(team1, team6)
    match2_results = match(team4, team7)
    match3_results = match(team2, team8)
    match4_results = match(team3, team5)
    #print("round 1")
    #print(match1_results)
    #print(match2_results)
    #print(match3_results)
    #print(match4_results)
    #print()
    # winners semis
    
    match5_results = match(match1_results.winner, match2_results.winner)
    match6_results = match(match3_results.winner, match4_results.winner)
    #print("Winners Semis")
    #print(match5_results)
    #print(match6_results)
    #print()
    # first losers
    match7_results = match(match1_results.loser, match2_results.loser)
    match8_results = match(match3_results.loser, match4_results.loser)
    #print("Losers , round 1")
    #print(match7_results)
    #print(match8_results)
    #print()
    # winners finals
    match9_results = match(match5_results.winner, match6_results.winner)
    #print("Winners Finals")
    #print(match9_results)
    #print()
    # second losers
    match10_results = match(match6_results.loser, match7_results.winner)
    match11_results = match(match5_results.loser, match8_results.winner)
    #print("losers round 2")
    #print(match10_results)
    #print(match11_results)
    #print()
    # lowers semis
    match12_results = match(match10_results.winner, match11_results.winner)
    #print("losers semis")
    #print(match12_results)
    #print()
    # losers finals
    match13_results = match(match12_results.winner, match9_results.loser)
    #print("losers finals")
    #print(match13_results)
    #print()
    # grand finals
    final_results = finals(match13_results.winner, match9_results.winner)
    #print("Grand final")
    #print(final_results)

    #print()
    #print(f"Champions: {final_results.winner}")
    
    return {"round1_match1":str(match1_results),"round1_match2":str(match2_results),"round1_match3":str(match3_results),"round1_match4":str(match4_results),"winner_semi1":str(match5_results),"winner_semi2":str(match6_results),"losers1_match1":str(match7_results),"losers1_match2":str(match8_results),"winners_final":str(match9_results),"losers2_match1":str(match10_results),"losers2_match2":str(match11_results),"loser_semi":str(match12_results),"loser_finals":str(match13_results),"grand_finals":str(final_results)}

data=[]
for i in range(20000):
    data.append(tournament_graph())

df=pd.DataFrame(data)
print("Round 1 Match 1")
print(df["round1_match1"].value_counts().head(6))
print("Roun 1 Match 2")
print(df["round1_match2"].value_counts().head(6))
print("Roun 1 Match 3")
print(df["round1_match3"].value_counts().head(6))
print("Roun 1 Match 4")
print(df["round1_match4"].value_counts().head(6))
print("Grand Finals")
print(df["grand_finals"].value_counts().head(8))
