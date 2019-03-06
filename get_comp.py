import  bs4
import requests
import re
import json
import ast

print("************************************************")
print("IMAGINATION IS THE ESSENCE OF DISCOVERY")
print("************************************************")

match_urls=["https://www.winstonslab.com/matches/match.php?id=40"+str(i) for i in range(58,110)]

match_url=match_urls[13]
html_data=requests.get(match_url)
html_data.raise_for_status()

parsed_html=[line for line in html_data.text.split('\n') if 'heroStatsArr.concat' in line]
data=re.split(r"\(|\)",parsed_html[0])[1][1:-1]
players_tuple=ast.literal_eval(data)
for dic in players_tuple:
    print("-------------------------")
    print("team:"+str(dic['teamName']))
    print("player name:"+str(dic['playerName']))
    print("map : "+str(dic['gameNumber'])+" -- "+str(dic['map']))
    print("hero :  "+str(dic['hero']))
    print("time played "+str(int(dic['timePlayed']) // 60)+":"+str(int(dic['timePlayed'])% 60))
