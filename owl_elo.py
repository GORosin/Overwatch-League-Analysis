import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
import random
from sklearn.utils import shuffle

update_config=0
elo_reduction=0;
team_map_diff={"PHI":0,"LDN":0,"BOS":0,"NYE":0,"PAR":0,"GLA":0,
           "SHD":0,"DAL":0,"CDH":0,"VAL":0,"SEO":0,"HZS":0,
           "GZC":0,"TOR":0,"WAS":0,"HOU":0,"ATL":0,"FLA":0,
           "SFS":0,"VAN":0}

teams={"PHI":1000,"LDN":1000,"BOS":1000,"NYE":1000,"PAR":1000,"GLA":1000,
       "SHD":1000,"DAL":1000,"CDH":1000,"VAL":1000,"SEO":1000,"HZS":1000,
       "GZC":1000,"TOR":1000,"WAS":1000,"HOU":1000,"ATL":1000,"FLA":1000,
       "SFS":1000,"VAN":1000}
def update_scores(teamA,teamB,scoreA,scoreB,teams,update=30):
    QA=10**(teams[teamA]/400)
    QB=10**(teams[teamB]/400)
    QA,QB=(QA+elo_reduction*QB)/(1+elo_reduction),(QB+elo_reduction*QA)/(1+elo_reduction)
    
    ExpectedA=QA/(QA+QB)
    ExpectedB=QB/(QA+QB)
    #so two ways to calculate scores, either normalize them
    #normA=scoreA/(scoreA+scoreB)
    #normB=scoreB/(scoreA+scoreB)
    #or 1 for win 0 for loss 0.5 for draw
    if(scoreA==scoreB):
        normA,normB=0.5,0.5
    else:
        normA= 1 if scoreA>scoreB else 0
        normB=1 if scoreA<scoreB else 0
    teams[teamA]+=update*(normA-ExpectedA)
    teams[teamB]+=update*(normB-ExpectedB)

def loop_series(series,teams):
    teamA,teamB=series[0:2]
    for i in range(2,9,2):
        scoreA,scoreB=series[i:i+2]
        update_scores(teamA,teamB,scoreA,scoreB,teams,update_config)
    if not (series[10]==series[11]):
        update_scores(teamA,teamB,series[10],series[11],teams,update=update_config)

def loop_matchs(owl_data,teams):
    for series in owl_data.values:
        loop_series(series,teams)
    return

def rank_teams(iterations,update,stage="stage1",elo_coeff=0):
    global elo_reduction
    elo_reduction =elo_coeff
    global update_config
    update_config=update
    owl_data=pd.read_csv(str(stage)+".csv")
    #owl_data=shuffle(owl_data)
    #plot out how a team looks after every match

    #number of iterations

    for i in range(iterations):
        loop_matchs(owl_data,teams)
    
    #plt.plot(range(len(my_team)),my_team)
    #plt.show()
    #rankings= sorted(teams.items(), key=operator.itemgetter(1))

    #return rankings
    return teams

def inter_stage_ranking(iterations,update):
    stage_1=rank_teams(10,update,"stage1")
    stage_2=rank_teams(iterations,update,"stage2")
    team_rankings={}
    for k,v in stage_1.items():
        team_rankings[k]=0.2*stage_1[k]+0.8*stage_2[k]

    rankings=sorted(team_rankings.items(), key=operator.itemgetter(1))
    return rankings

if __name__=="__main__":
    rankings=inter_stage_ranking(20,5)
    for i in rankings[::-1]:
        print("team:"+str(i[0])+" elo:"+str(int(i[1])))

