import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
import random
from sklearn.utils import shuffle

update_config=0
penalty=0
elo_reduction=0;
def update_scores(teamA,teamB,scoreA,scoreB,teams,update=30):
    
    QA=10**(teams[teamA]/400)
    QB=10**(teams[teamB]/400)

    QA=(QA+elo_reduction*QB)/(1+elo_reduction)
    QB=(QB+elo_reduction*QA)/(1+elo_reduction)
    
    ExpectedA=QA/(QA+QB)
    ExpectedB=QB/(QA+QB)

    #so two ways to calculate scores, either normalize them
    #normA=scoreA/(scoreA+scoreB)
    #normB=scoreB/(scoreA+scoreB)

    #or 1 for win 0 for loss 0.5 for draw
    if(scoreA==scoreB):
        normA,normB=0.5,0.5
    else:
        normA=float(scoreA>scoreB)
        normB=float(scoreA<scoreB)
    teams[teamA]+=update*(normA-ExpectedA)
    teams[teamB]+=update*(normB-ExpectedB)

def loop_series(series,teams):
    teamA,teamB=series[0:2]
    score=0
    for i in range(2,9,2):
        scoreA,scoreB=series[i:i+2]
        if(score==3 or score ==-3):
            update_scores(teamA,teamB,scoreA,scoreB,teams,update=update_config*penalty)
        else:
            update_scores(teamA,teamB,scoreA,scoreB,teams,update_config)
        score+=int(scoreA>scoreB)-int(scoreA<scoreB)

    if not (series[9]==series[10]):
        update_scores(teamA,teamB,series[9],series[10],teams)

def loop_matchs(owl_data,teams):
    for series in owl_data.values:
        loop_series(series,teams)
    return

def rank_teams(iterations,update,map_penalty,elo_coeff=0):
    global elo_reduction=elo_coeff
    global teams
    global penalty
    penalty=map_penalty
    global update_config
    update_config=update
    owl_data=pd.read_csv("owl_scores.csv")
    #owl_data=shuffle(owl_data)
    #plot out how a team looks after every match

    #number of iterations
    teams={"PHI":1000,"LDN":1000,"BOS":1000,"NYE":1000,"PAR":1000,"GLA":1000,
           "SHD":1000,"DAL":1000,"CDH":1000,"VAL":1000,"SEO":1000,"HZS":1000,
           "GZC":1000,"TOR":1000,"WAS":1000,"HOU":1000,"ATL":1000,"FLA":1000,
           "SFS":1000,"VAN":1000}
    for i in range(iterations):
        loop_matchs(owl_data,teams)
    
    #plt.plot(range(len(my_team)),my_team)
    #plt.show()
    rankings= sorted(teams.items(), key=operator.itemgetter(1))
    '''
    for i in rankings[::-1]:
        print("team:"+str(i[0])+" elo:"+str(int(i[1])))
    '''
    return rankings
