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

features=["away_main_dps_kills","away_main_dps_deaths","away_main_dps_ults","away_main_dps_kdr","away_flex_dps_kills","away_flex_dps_deaths","away_flex_dps_ults","away_flex_dps_kdr","away_main_support_kills","away_main_support_deaths","away_main_support_ults","away_main_support_kdr","away_flex_support_kills","away_flex_support_deaths","away_flex_support_ults","away_flex_support_kdr","away_main_tank_kills","away_main_tank_deaths","away_main_tank_ults","away_main_tank_kdr","away_flex_tank_kills","away_flex_tank_deaths","away_flex_tank_ults","away_flex_tank_kdr","home_main_dps_kills","home_main_dps_deaths","home_main_dps_ults","home_main_dps_kdr","home_flex_dps_kills","home_flex_dps_deaths","hom_flex_dps_ults","hom_flex_dps_kdr","home_main_support_kills","hom_main_support_deaths","hom_main_support_ults","hom_main_support_kdr","home_flex_support_kills","hom_flex_support_deaths","hom_flex_support_ults","hom_flex_support_kdr","home_main_tank_kills","hom_main_tank_deaths","hom_main_tank_ults","hom_main_tank_kdr","home_flex_tank_kills","hom_flex_tank_deaths","hom_flex_tank_ults","hom_flex_tank_kdr","away_team_goats","away_team_Winston_goats","away_team_sombra_goats","away_team_ana_goats","away_team_dive","away_team_wrecking_crew","home_team_goats","home_team_Winston_goats","home_team_sombra_goats","home_team_ana_goats","home_team_dive","home_team_wrecking_crew"]

def train(x,y,shape):
    nn_win_model=create_model(shape)
    print(x.shape)
    print(y.shape)
    nn_win_model.fit(x,y,epochs=500, batch_size=30)
    return nn_win_model

def one_hot_encode(value,size=20):
    arr=np.zeros(size)
    arr[teams[value]-1]=1
    return arr

def create_model(shape):
    model=Sequential()
    model.add(Dense(shape,input_dim=shape,kernel_initializer='normal',activation='sigmoid'))
    model.add(Dense(8,activation='sigmoid'))
    model.add(Dense(3,activation='sigmoid'))

    model.add(Dense(2,kernel_initializer='normal',activation='softmax'))
    opt=Adam(lr=0.2,decay=0.09)
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
        results+=(prediction[0]-label[0])**2
        if pred_winner==actual_winner:
            correct+=1
        print(prediction)
        print(label)
        indx+=1
    print("correct: "+str(correct))
    print("total: "+str(indx))
    return results
def create_labels():
    score_data=pd.read_csv("stage1_results.csv")
    team_data=pd.read_csv("winston_data.csv")
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
    
    close=[135,5,112,245,257,115,269,169]
    clear_win=[189,205,221,269,11,253,132,144]
    stomps=[127,26,51,126,162,3,81,128]
    
    train_data=np.ones(len(y),dtype=bool)
    test_data=np.zeros(len(y),dtype=bool)
    for idx in stomps:
        train_data[idx]=False
        test_data[idx]=True


    x_train=X[train_data]
    y_train=y[train_data]
    x_test=X[test_data]
    y_test=y[test_data]
    team_tests=teams[test_data]
    print(team_tests)
    print(y_test)

    
    model=train(x_train,y_train,n_comp)
    results=accuracy(model,x_test,y_test)
    return results
    

main_test(4)

    
       
