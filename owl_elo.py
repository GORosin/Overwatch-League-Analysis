import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
import random
from sklearn.utils import shuffle

teams={"PHI":1000,"LDN":1000,"BOS":1000,"NYE":1000,"PAR":1000,"GLA":1000,"SHD":1000,"DAL":1000,"CDH":1000,"VAL":1000,"SEO":1000,"HZS":1000,"GZC":1000,"TOR":1000,"WAS":1000,"HOU":1000,"ATL":1000,"FLA":1000,"SFS":1000,"VAN":1000}

my_team=[1000]
team_name='DAL'
def update_scores(teamA,teamB,scoreA,scoreB,update=32):
    global teams
    QA=10**(teams[teamA]/400)
    QB=10**(teams[teamB]/400)
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

def loop_series(series):
    teamA,teamB=series[0:2]
    for i in range(2,9,2):
        scoreA,scoreB=series[i:i+2]
        update_scores(teamA,teamB,scoreA,scoreB)

    if not (series[9]==series[10]):
        update_scores(teamA,teamB,series[9],series[10],)

def loop_matchs(owl_data):
    global teams
    global team_name
    global my_team
    for series in owl_data.values[::-1]:
        loop_series(series)
        if team_name in series[0:2]:
            print(series[0:2])
            my_team.append(teams[team_name])
    return

def rank_teams():
    global teams
    owl_data=pd.read_csv("owl_scores.csv")
    owl_data=shuffle(owl_data)
    #plot out how a team looks after every match

    #number of iterations
    for i in range(1):
        loop_matchs(owl_data)
    
    plt.plot(range(len(my_team)),my_team)
    plt.show()
    rankings= sorted(teams.items(), key=operator.itemgetter(1))
    for i in rankings[::-1]:
        print("team:"+str(i[0])+" elo:"+str(i[1]))

def flip_coin(p):
    return int(random.random() < p)

def simulate_series(p_a):
    score_a=0
    score_b=0
    for i in range(4):
        results=flip_coin(p_a)
        score_a+=results
        score_b+=1-results
    if(score_a==score_b):
        result=flip_coin(p_a)
        score_a+=result
        score_b+=1-result
    return (score_a,score_b)

def calc_mean(dist):
    return np.sum(dist*np.linspace(0,4,5))

def predict(teamA,teamB):
    #using monte carlo
    p_a=1/(1+10**((teams[teamB]-teams[teamA])/400))
    scores_A=np.zeros(5)
    scores_B=np.zeros(5)
    for i in range(100000):
        a,b=simulate_series(p_a)
        scores_A[a]+=1
        scores_B[b]+=1
    scores_A=scores_A/np.sum(scores_A)
    scores_B=scores_B/np.sum(scores_B)
    print(scores_A)
    print(calc_mean(scores_A),calc_mean(scores_B))
    plt.bar(np.linspace(0,4,5),scores_A,label=teamA)
    plt.bar(np.linspace(0,4,5),scores_B,label=teamB,alpha=0.5)
    plt.legend()
    plt.show()

rank_teams()
#predict('NYE',"CDH")
def tie_study():
    rates=[42.0,12.0,40.0,19.0]
    probs=[1/(1+10**(i/400.0)) for i in rates]
    print(probs)

