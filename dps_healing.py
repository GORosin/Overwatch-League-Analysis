import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from sklearn.mixture import GaussianMixture as cluster


data=pd.read_csv("dps_healing.txt", sep=r"\s*",engine='python')
print(data[['Heals','Damage','Deaths']].head(5))
fig, axis = plt.subplots(3)
ax,ay,az=axis
y_attr="Heals"
x_attr="Deaths"

clusters=cluster(4)
clusters.fit(data[['Heals','Damage','Deaths']])

colmap={0:"k",1:"r",2:"b",3:"y"}
colors=[clusters.predict(row.reshape(1,-1))[0] for row in data[['Heals','Damage','Deaths']].values]
print(colors)
#ax.scatter(data[x_attr], data[y_attr],c=colors)

ax.scatter(data['Damage'], data['Deaths'],c=colors)
for i, txt in enumerate(data['Name']):
    ax.annotate(txt, (data.iloc[i]['Damage'], data.iloc[i]['Deaths']))
ax.set_xlabel('Damage')
ax.set_ylabel('Deaths')

ay.scatter(data['Heals'], data['Damage'],c=colors)
ay.set_xlabel('Heals')
ay.set_ylabel('Damage')
for i, txt in enumerate(data['Name']):
    ay.annotate(txt, (data.iloc[i]['Heals'], data.iloc[i]['Damage']))

az.scatter(data['Heals'], data['Deaths'],c=colors)
az.set_xlabel('Heals')
az.set_ylabel('Deaths')
for i, txt in enumerate(data['Name']):
    az.annotate(txt, (data.iloc[i]['Heals'], data.iloc[i]['Deaths']))
plt.show()


'''
legend_elements = [Line2D([0], [0], marker='o', color='w', label='top 5',
                          markerfacecolor='y', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='middle-top 5',
                          markerfacecolor='b', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='middle-bottom 5',
                          markerfacecolor='r', markersize=15),
                     Line2D([0], [0], marker='o', color='w', label='bottom 5',
                          markerfacecolor='k', markersize=15)]
#ax.legend(handles=legend_elements)
'''

