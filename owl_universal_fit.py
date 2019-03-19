#inspired by (shamelessly ripped off from) https://github.com/franckjay/BayesianOverwatchElo/blob/master/overwatch-elo-ratings-pymc3.ipynb

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

import numpy as np
import matplotlib.pyplot as plt
import pymc3 as pm
import pandas as pd
import operator
import theano.tensor as tt


teams={"PHI":0,"LDN":1,"BOS":2,"NYE":3,"PAR":4,"GLA":5,"SHD":6,"DAL":7,"CDH":8,"VAL":9,"SEO":10,"HZS":11,"GZC":12,"TOR":13,"WAS":14,"HOU":15,"ATL":16,"FLA":17,"SFS":18,"VAN":19}

data=pd.read_csv("owl_scores.csv")
team1=[]
team2=[]
scores=[]
##reading data, not interesting ############
def loop_series(series,team1,team2,score):
    teamA,teamB=series[0:2]
    for i in range(2,9,2):
        scoreA,scoreB=series[i:i+2]
        team1.append(teams[teamA])
        team2.append(teams[teamB])
        score.append(.99 if scoreA > scoreB else 0.01)
    if not (series[10]==series[11]):
        scoreA,scoreB=series[10:12]
        team1.append(teams[teamA])
        team2.append(teams[teamB])
        score.append(0.99 if scoreA > scoreB else 0.01)
def loop_matchs(owl_data,team1,team2,score):
    for series in owl_data.values:
        loop_series(series,team1,team2,score)
    return

loop_matchs(data,team1,team2,scores)
team1_index=np.array(team1)
team2_index=np.array(team2)
model_output=np.array(scores)


######model parameters tune alpha, beta parameters here
elo_model= pm.Model()
with elo_model:
    sigma = pm.Gamma('noise', alpha=10.0, beta=0.05)
    elo_team=pm.Normal('elo_team',mu=1000,sd=sigma,shape=20)
    log_rating1 = 10.0**(elo_team[team1_index]/400.0)
    log_rating2 = 10.0**(elo_team[team2_index]/400.0)
    E = log_rating1/(log_rating1+log_rating2) # Expected value
    error =  pm.HalfCauchy('error', beta=1.0)
    out = pm.Normal('out', mu=E, sd = error, observed=model_output)

##number of saples, again tune here
with elo_model:
    step = pm.Slice()
    trace = pm.sample(3000,step=step)


    
#pm.traceplot(trace)
#plt.show()
#print rakings
stats=np.array(pm.summary(trace)['mean'])[:20]
reversed_teams={v:k for k,v in teams.items()}
team_ranks={reversed_teams[i]:stats[i] for i in range(20)}
rankings= sorted(team_ranks.items(), key=operator.itemgetter(1))
for i in rankings[::-1]:
    print("team:"+str(i[0])+" elo:"+str(int(i[1])))
