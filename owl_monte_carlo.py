import matplotlib.pyplot as plt
import numpy as np
from owl_elo import rank_teams,teams
import random
from th1 import hist1d
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
    rank_teams(10,30)
    print(teams)
    #using monte carlo
    p_a=1/(1+10**((teams[teamB]-teams[teamA])/400))
    
    index={-4:1,-2:2,-1:3,1:4,2:5,4:6}
    scores_A=np.zeros(5)
    scores_B=np.zeros(5)
    A_hist=hist1d(6,1,7)
    B_hist=hist1d(6,1,7)
    iterations=100000
    for i in range(iterations):
        a,b=simulate_series(p_a)
        A_hist.fill(index[a-b])
        B_hist.fill(index[b-a])
        scores_A[a]+=1
        scores_B[b]+=1
    scores_A=scores_A/np.sum(scores_A)
    scores_B=scores_B/np.sum(scores_B)
    print(scores_A)
    print(calc_mean(scores_A),calc_mean(scores_B))
    print(A_hist.data)
    plt.ylim(0,0.6)
    plt.bar(np.linspace(1,6,6),A_hist.data[1:-1]/iterations,width=0.30,label=teamA)
    plt.bar(np.linspace(1,6,6)+0.30,B_hist.data[1:-1]/iterations,width=0.30,label=teamB)
    plt.xticks(np.linspace(1,6,6)+ 0.3, ('0-4', '1-3', '2-3', '3-1','3-1','4-0'))
    plt.text(2.2,.5,"Team A Win:"+str(round(np.sum(A_hist.data[4:7]/iterations),2))+" team B Wins:"+str(round(np.sum(A_hist.data[1:4]/iterations),2)),bbox=dict(boxstyle="round",ec=(1., 0.5, 0.5),fc=(1., 0.8, 0.8),))
    plt.legend()
    plt.show()

def tie_study():
    rates=[42.0,12.0,40.0,19.0]
    probs=[1/(1+10**(i/400.0)) for i in rates]
    print(probs)

if __name__ == '__main__':
    predict("LDN","PHI")
