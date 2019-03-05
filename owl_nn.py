from numpy.random import shuffle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Dropout
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import pandas as pd
from keras.optimizers import Adagrad

teams={"PHI":1,"LDN":2,"BOS":3,"NYE":4,"PAR":5,"GLA":6,"SHD":7,"DAL":8,"CDH":9,"VAL":10,"SEO":11,"HZS":12,"GZC":13,"TOR":14,"WAS":15,"HOU":16,"ATL":17,"FLA":18,"SFS":19,"VAN":20}

def train(data):
    for indx,series in enumerate(data.values):
        score_teamA,score_teamB=series[6:8]
        x[indx][0:20]=one_hot_encode(series[0])
        x[indx][20:40]=one_hot_encode(series[1])
        x[indx][40:44]=series[2:6]
    
        y[indx][0]=int(score_teamA>score_teamB)
        y[indx][1]=int(score_teamA<score_teamB)


    nn_win_model=model()
    nn_win_model.fit(x,y,epochs=400, batch_size=32)
    return nn_win_model

def one_hot_encode(value,size=20):
    arr=np.zeros(size)
    arr[teams[value]-1]=1
    return arr

def model():
    model=Sequential()
    #model.add(Dropout(0.2,input_shape=(4,)))
    model.add(Dense(4,input_dim=4,kernel_initializer='normal',activation='sigmoid'))
   # model.add(Dense(50,activation='relu'))
   # model.add(Dropout(0.2))
   # model.add(Dense(25,activation='relu'))
   # model.add(Dropout(0.1))
   # model.add(Dense(15,activation='relu'))
    model.add(Dense(3,activation='relu'))
    model.add(Dense(2,kernel_initializer='normal',activation='softmax'))
    opt=Adagrad(decay=0.001)
    model.compile(loss='categorical_crossentropy',optimizer=opt)
    return model

win_data=pd.read_csv("owl_scores.csv")
data=pd.read_csv("map_stats.csv")

#data=pd.read_csv("series_stats.csv")
x=np.zeros((len(data.index)*4,4))
y=np.zeros((len(x),2),dtype=float)
indx=0
for j,series in enumerate(data.values):
    teamA,teamB=series[0:2]
    for i in range(2,17,4):
        #x[indx][0:20]=one_hot_encode(teamA)
        #x[indx][20:40]=one_hot_encode(teamB)
        x[indx][0:4]=series[i:i+4]
        #x[indx][40]=x[indx][40]/(x[indx][40]+x[indx][41])*100
        #x[indx][41]=x[indx][41]/(x[indx][40]+x[indx][41])*100
        #x[indx][42]=x[indx][42]/(x[indx][42]+x[indx][43])*12
        #x[indx][43]=x[indx][43]/(x[indx][42]+x[indx][43])*12
        score_teamA,score_teamB=win_data.iloc[j,2+(i-2)//2:4+(i-2)//2]
        y[indx][0]=int(score_teamA>score_teamB)
        y[indx][1]=int(score_teamA<score_teamB)
        indx+=1

nn_win_model=model()
nn_win_model.fit(x,y,epochs=400, batch_size=32)
#boston vs. houston
teamA='PHI'
teamB='LDN'

map1_stat=np.array([30,27,8,5])
map1=np.zeros(44)
map1[0:20]=one_hot_encode(teamA)
map1[20:40]=one_hot_encode(teamB)
map1[40:44]=map1_stat

map2_stat=np.array([47,65,9,12])
map2=np.zeros(44)
map2[0:20]=one_hot_encode(teamA)
map2[20:40]=one_hot_encode(teamB)
map2[40:44]=map2_stat

map3_stat=np.array([40,57,6,12])
map3=np.zeros(44)
map3[0:20]=one_hot_encode(teamA)
map3[20:40]=one_hot_encode(teamB)
map3[40:44]=map3_stat

map4_stat=np.array([24,5,6,0])
map4=np.zeros(44)
map4[0:20]=one_hot_encode(teamA)
map4[20:40]=one_hot_encode(teamB)
map4[40:44]=map4_stat

#map5_stat=np.array([34,36,7,6])
#map5=np.zeros(44)
#map5[0:20]=one_hot_encode(teamA)
#map5[20:40]=one_hot_encode(teamB)
#map5[40:44]=map5_stat

print(nn_win_model.predict(map1_stat.reshape(1,-1)))
print(nn_win_model.predict(map2_stat.reshape(1,-1)))
print(nn_win_model.predict(map3_stat.reshape(1,-1)))
print(nn_win_model.predict(map4_stat.reshape(1,-1)))
#print(nn_win_model.predict(map5.reshape(1,-1)))


count=0
win=0
for indx in range(len(x)):
    x_data=x[indx]
    y_data=y[indx]
    '''
    print("----------------------------")
    print(nn_win_model.predict(x_data.reshape(1,-1)))
    print(y_data)
    print("------------------------------")
    '''
    nn_win_model.predict(x_data.reshape(1,-1))
    count+=1
    if(np.argmax(nn_win_model.predict(x_data.reshape(1,-1)))==np.argmax(y_data)):
        win+=1
print(win)
print(count)
