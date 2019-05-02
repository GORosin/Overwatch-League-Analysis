from numpy.random import shuffle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Dropout
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import pandas as pd
from keras.optimizers import Adagrad,Adam
from sklearn.decomposition import PCA

teams={"PHI":1,"LDN":2,"BOS":3,"NYE":4,"PAR":5,"GLA":6,"SHD":7,"DAL":8,"CDH":9,"VAL":10,"SEO":11,"HZS":12,"GZC":13,"TOR":14,"WAS":15,"HOU":16,"ATL":17,"FLA":18,"SFS":19,"VAN":20}

def train(x,y,shape):
    nn_win_model=create_model(shape)
    print(x.shape)
    print(y.shape)
    nn_win_model.fit(x,y,epochs=200, batch_size=30)
    return nn_win_model

def one_hot_encode(value,size=20):
    arr=np.zeros(size)
    arr[teams[value]-1]=1
    return arr

def create_model(shape):
    model=Sequential()
    model.add(Dense(shape,input_dim=shape,kernel_initializer='normal',activation='sigmoid'))
    model.add(Dense(6,activation='sigmoid'))
    model.add(Dense(2,kernel_initializer='normal',activation='softmax'))
    opt=Adam(lr=0.04,decay=0.01)
    model.compile(loss='categorical_crossentropy',optimizer=opt)
    return model

def accuracy(trained_model,data,labels):
    correct=0
    indx=0
    results=0
    for datum,label in zip(data,labels):
        prediction=trained_model.predict(datum.reshape(1,-1))[0]
        pred_winner=int(prediction[0] > prediction[1])
        actual_winner=int(label[0] > label[1])
        if pred_winner==actual_winner:
            correct+=1
        print(prediction)
        results+=(prediction[0]-label[0])**2
        print(label)
        indx+=1
    print("correct: "+str(correct))
    print("total: "+str(indx))
    return results
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
def main_test(n_comp):
    reduce_data=PCA(n_comp)
    X_full,y,teams=create_labels()
    X=reduce_data.fit_transform(X_full)
    ties=[6, 77, 106, 131, 156, 231, 239, 260, 265]
    train_data=np.ones(len(y),dtype=bool)
    test_data=np.zeros(len(y),dtype=bool)
    for idx in ties:
        train_data[idx]=False
        test_data[idx]=True
    
    x_train=X[0:200]
    y_train=y[0:200]
    x_test=X[200:]
    y_test=y[200:]
    model=train(x_train,y_train,n_comp)
    results=accuracy(model,x_test,y_test)
    return results

print(main_test(4))
