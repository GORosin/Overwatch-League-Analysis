import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
class hist1d:
    def __init__(self,nbins,xmin,xmax):
        self.nbins=nbins
        self.xmax=xmax
        self.xmin=xmin
        self.data=np.zeros(nbins+2)

    def _num_to_index(self,num):
        if num <self.xmin:
            return 0
        elif num >=self.xmax:
            return self.nbins+1
        else:
            return int(self.nbins*(num-self.xmin)/(self.xmax-self.xmin))+1

    def fill(self,num,weight=1):
        self.data[self._num_to_index(num)]+=weight

    def draw(self,offset=0):
        plt.bar(np.linspace(self.xmin,self.xmax,self.nbins),self.data[1:-1],align='edge',width=1000/self.nbins+offset,edgecolor='black')
    


class hist2d:
    def __init__(self,xnbins,xmin,xmax,ynbins,ymin,ymax):
        self.nxbins=nxbins
        self.xmax=xmax
        self.xmin=xmin
        self.data=np.zeros(nxbins+2,nybins+2)
        self.nybins=nybins
        self.ymax=ymax
        self.ymin=ymin
        
    def _x_num_to_index(self,num):
        if num <self.xmin:
            return 0
        elif num > self.xmax:
            return self.nxbins+1
        else:
            return int(self.nxbins*(num-self.xmin)/(self.xmax-self.xmin))+1

    def _y_num_to_index(self,num):
        if num <self.ymin:
            return 0
        elif num > self.ymax:
            return self.nybins+1
        else:
            return int(self.nybins*(num-self.ymin)/(self.ymax-self.ymin))+1

    def fill(x,y,weight=1):
        self.data[_x_num_to_index[x], _y_num_to_index[y]]+=weight
