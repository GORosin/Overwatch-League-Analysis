from scipy.optimize import curve_fit
from math import exp
import numpy as np
import matplotlib.pyplot as plt
def logistic(x,k=17.95):
    return 1/(1+np.exp(-1*x/k))

team_elo={"DAL":121,"SHD":120,"GLA":117,"ATL":114,"CDH":111,"SFS":111,"WAS":107,"HOU":106,"PHL":104,"TOR":102,"SEO":99,"PAR":99,"BOS":97,"HZS":96,"FLR":96,"NYXL":93,"GZC":87,"LDN":81,"VAN":73,"LAV":64}

def estimate_logistic():
    vs_dallas={"ATL":0.55,"BOS":0.95,"FLR":0.95,"GLA":0.51,"LDN":0.99,"PAR":0.75,"SFS":0.55,"TOR":0.85,"VAN":0.99,"WAS":0.6}

    vs_dragon={"CDH":0.6,"GZC":0.9,"HZS":0.75,"LAV":0.999,"NYXL":0.7,"PHL":0.55,"SEO":0.65}
    
    d_xy=[(team_elo["DAL"]-team_elo[key],value,key) for key,value in vs_dallas.items()] 
    sh_xy=[(team_elo["SHD"]-team_elo[key],value,key) for key,value in vs_dragon.items()]
    xy_total=d_xy+sh_xy
    X=np.array([i[0] for i in xy_total]+[-1*i[0] for i in xy_total])
    Y=np.array([i[1] for i in xy_total]+[1-i[1] for i in xy_total])
    labels=[i[2] for i in xy_total]+[i[2] for i in xy_total]
    results,cov=curve_fit(logistic,X,Y)
    print(results)
    X_fit=np.linspace(-70,70,100)
    Y_fit1=logistic(X_fit,17.95)
    Y_fit2=logistic(X_fit,20)
    Y_fit3=logistic(X_fit,22)
    Y_fit4=logistic(X_fit,12)
    Y_fit5=logistic(X_fit,10)
    plt.plot(X_fit,Y_fit1)
    plt.plot(X_fit,Y_fit2)
    plt.plot(X_fit,Y_fit3)
    plt.plot(X_fit,Y_fit4)
    plt.plot(X_fit,Y_fit5)
    plt.plot(X,Y,".")
    plt.ylabel("Probablity of team 1 winning")
    plt.xlabel("Power Ranking difference team 1 - team 2")
    #plt.savefig("elo_probality_estimate")
    for idx,(i,j) in enumerate(zip(X,Y)):
        plt.annotate(labels[idx],xy=(i,j),ha='center')
    plt.show()

estimate_logistic()
