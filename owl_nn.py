from numpy.random import shuffle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Dropout
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import pandas as pd


teams={"PHI":1,"LDN":2,"BOS":3,"NYE":4,"PAR":5,"GLA":6,"SHD":7,"DAL":8,"CDH":9,"VAL":10,"SEO":11,"HZS":12,"GZC":13,"TOR":14,"WAS":15,"HOU":16,"ATL":17,"FLA":18,"SFS":19,"VAN":20}

def one_hot_encode(value,size=20):
    arr=np.zeros(size)
    arr[teams[value]-1]=1
    return arr

def model():
    model=Sequential()
    model.add(Dropout(0.4,input_shape=(44,)))
    model.add(Dense(44,input_dim=44,kernel_initializer='normal',activation='relu'))
    model.add(Dense(50,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(25,activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(10,activation='relu'))
    model.add(Dense(2,kernel_initializer='normal',activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer='adam')
    return model


data=pd.read_csv("series_stats.csv")
x=np.zeros((len(data.index),44))
y=np.zeros((len(x),2),dtype=float)


for indx,series in enumerate(data.values):
    score_teamA,score_teamB=series[6:8]
    x[indx][0:20]=one_hot_encode(series[0])
    x[indx][20:40]=one_hot_encode(series[1])
    x[indx][40:44]=series[2:6]
    
    y[indx][0]=int(score_teamA>score_teamB)
    y[indx][1]=int(score_teamA<score_teamB)


nn_win_model=model()
nn_win_model.fit(x,y,epochs=400, batch_size=32)
'''
#boston vs. houston
map1_stat=np.array([34,6,7,1])
map1=np.zeros(44)
map1[0:20]=one_hot_encode('HOU')
map1[20:40]=one_hot_encode('BOS')
map1[40:44]=map1_stat

map2_stat=np.array([48,45,12,9])
map2=np.zeros(44)
map2[0:20]=one_hot_encode('HOU')
map2[20:40]=one_hot_encode('BOS')
map2[40:44]=map2_stat

map3_stat=np.array([39,55,8,11])
map3=np.zeros(44)
map3[0:20]=one_hot_encode('HOU')
map3[20:40]=one_hot_encode('BOS')
map3[40:44]=map3_stat

map4_stat=np.array([64,40,12,7])
map4=np.zeros(44)
map4[0:20]=one_hot_encode('HOU')
map4[20:40]=one_hot_encode('BOS')
map4[40:44]=map4_stat

map5_stat=np.array([34,36,7,6])
map5=np.zeros(44)
map5[0:20]=one_hot_encode('HOU')
map5[20:40]=one_hot_encode('BOS')
map5[40:44]=map5_stat

print(nn_win_model.predict(map1.reshape(1,-1)))
print(nn_win_model.predict(map2.reshape(1,-1)))
print(nn_win_model.predict(map3.reshape(1,-1)))
print(nn_win_model.predict(map4.reshape(1,-1)))
print(nn_win_model.predict(map5.reshape(1,-1)))
'''
''''
#Vancouver vs. san francisco
#boston vs. houston
map1_stat=np.array([29,21,6,5])
map1=np.zeros(44)
map1[0:20]=one_hot_encode('VAN')
map1[20:40]=one_hot_encode('SFS')
map1[40:44]=map1_stat

map2_stat=np.array([49,59,13,15])
map2=np.zeros(44)
map2[0:20]=one_hot_encode('VAN')
map2[20:40]=one_hot_encode('SFS')
map2[40:44]=map2_stat

map3_stat=np.array([49,25,11,3])
map3=np.zeros(44)
map3[0:20]=one_hot_encode('VAN')
map3[20:40]=one_hot_encode('SFS')
map3[40:44]=map3_stat

map4_stat=np.array([70,54,15,14])
map4=np.zeros(44)
map4[0:20]=one_hot_encode('VAN')
map4[20:40]=one_hot_encode('SFS')
map4[40:44]=map4_stat


print(nn_win_model.predict(map1.reshape(1,-1)))
print(nn_win_model.predict(map2.reshape(1,-1)))
print(nn_win_model.predict(map3.reshape(1,-1)))
print(nn_win_model.predict(map4.reshape(1,-1)))
'''


'''
map1_stat=np.array([41,28,10,7])
map1=np.zeros(44)
map1[0:20]=one_hot_encode('TOR')
map1[20:40]=one_hot_encode('VAL')
map1[40:44]=map1_stat

map2_stat=np.array([61,69,14,13])
map2=np.zeros(44)
map2[0:20]=one_hot_encode('TOR')
map2[20:40]=one_hot_encode('VAL')
map2[40:44]=map2_stat

map3_stat=np.array([59,40,9,9])
map3=np.zeros(44)
map3[0:20]=one_hot_encode('TOR')
map3[20:40]=one_hot_encode('VAL')
map3[40:44]=map3_stat

map4_stat=np.array([40,48,8,10])
map4=np.zeros(44)
map4[0:20]=one_hot_encode('TOR')
map4[20:40]=one_hot_encode('VAL')
map4[40:44]=map4_stat


print(nn_win_model.predict(map1.reshape(1,-1)))
print(nn_win_model.predict(map2.reshape(1,-1)))
print(nn_win_model.predict(map3.reshape(1,-1)))
print(nn_win_model.predict(map4.reshape(1,-1)))
'''

map1_stat=np.array([19,46,4,9])
map1=np.zeros(44)
map1[0:20]=one_hot_encode('CDH')
map1[20:40]=one_hot_encode('GZC')
map1[40:44]=map1_stat

map2_stat=np.array([41,38,9,7])
map2=np.zeros(44)
map2[0:20]=one_hot_encode('CDH')
map2[20:40]=one_hot_encode('GZC')
map2[40:44]=map2_stat

map3_stat=np.array([22,65,4,12])
map3=np.zeros(44)
map3[0:20]=one_hot_encode('CDH')
map3[20:40]=one_hot_encode('GZC')
map3[40:44]=map3_stat

map4_stat=np.array([52,48,11,7])
map4=np.zeros(44)
map4[0:20]=one_hot_encode('CDH')
map4[20:40]=one_hot_encode('GZC')
map4[40:44]=map4_stat

map5_stat=np.array([35,31,11,6])
map5=np.zeros(44)
map5[0:20]=one_hot_encode('CDH')
map5[20:40]=one_hot_encode('GZC')
map5[40:44]=map5_stat


print(nn_win_model.predict(map1.reshape(1,-1)))
print(nn_win_model.predict(map2.reshape(1,-1)))
print(nn_win_model.predict(map3.reshape(1,-1)))
print(nn_win_model.predict(map4.reshape(1,-1)))
print(nn_win_model.predict(map5.reshape(1,-1)))

'''

for indx in range(len(x)):
    x_data=x[indx]
    print(data.loc[indx,"A":"B"])
    y_data=y[indx]
    print("----------------------------")
    print(nn_win_model.predict(x_data.reshape(1,-1)))
    print(y_data)
    print("------------------------------")



'''
