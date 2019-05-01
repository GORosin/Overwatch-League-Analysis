from numpy.random import shuffle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Dropout
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import pandas as pd
from keras.optimizers import Adagrad,Adam

teams={"PHI":1,"LDN":2,"BOS":3,"NYE":4,"PAR":5,"GLA":6,"SHD":7,"DAL":8,"CDH":9,"VAL":10,"SEO":11,"HZS":12,"GZC":13,"TOR":14,"WAS":15,"HOU":16,"ATL":17,"FLA":18,"SFS":19,"VAN":20}

def train(x,y):
    nn_win_model=create_model()
    print(x.shape)
    print(y.shape)
    nn_win_model.fit(x,y,epochs=1000, batch_size=30)
    return nn_win_model

def one_hot_encode(value,size=20):
    arr=np.zeros(size)
    arr[teams[value]-1]=1
    return arr

def create_model():
    model=Sequential()
    model.add(Dense(60,input_dim=60,kernel_initializer='normal',activation='sigmoid'))
    model.add(Dense(70,activation='sigmoid'))
    model.add(Dense(30,activation='sigmoid'))
    model.add(Dense(15,activation='sigmoid'))
    model.add(Dense(7,activation='sigmoid'))
    model.add(Dense(2,kernel_initializer='normal',activation='softmax'))
    opt=Adam(lr=0.1,decay=0.09)
    model.compile(loss='categorical_crossentropy',optimizer=opt)
    return model

def accuracy(trained_model,data,labels,teams):
    correct=0
    indx=0
    for datum,label in zip(data,labels):
        prediction=trained_model.predict(datum.reshape(1,-1))[0]
        pred_winner=int(prediction[0] > prediction[1])
        actual_winner=int(label[0] > label[1])
        if pred_winner==actual_winner:
            correct+=1
        else:
            pass
            print(prediction)
            print(label)
            print(teams.ix[indx,:])
        indx+=1
    print("correct: "+str(correct))
    print("total: "+str(indx))
    
def create_labels():
    score_data=pd.read_csv("stage1_results.csv")
    team_data=pd.read_csv("winston_data.csv")
    print(team_data.shape)
    X=np.zeros(shape=[team_data.shape[0],team_data.shape[1]-3],dtype=np.float64)
    y=np.zeros((len(score_data),2),dtype=np.float64)
    idx=0
    for data,label in zip(team_data.loc[:,"away_main_dps_kills":"home_team_wrecking_crew"].values,score_data.loc[:,"scoreA":"scoreB"].values):
        X[idx][:]=data[:]

        if label[0] > label[1]:
            y[idx][0]=1
        elif label[0] < label[1]:
            y[idx][1]=1
        else:
            y[idx][0]=0.5
            y[idx][1]=0.5
        idx+=1

    return X,y,score_data.loc[:,"teamA":"teamB"]

X,y,teams=create_labels()
model=train(X[:200],y[:200])
accuracy(model,X[200:],y[200:],teams)
