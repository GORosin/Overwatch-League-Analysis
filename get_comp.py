import  bs4
import requests
import re
import json
import ast

print("************************************************")
print("IMAGINATION IS THE ESSENCE OF DISCOVERY")
print("************************************************")

match_urls=["https://www.winstonslab.com/matches/match.php?id=40"+str(i) for i in range(58,110)]

match_url=match_urls[0]
html_data=requests.get(match_url)
print(match_url)
html_data.raise_for_status()

parsed_html=[line for line in html_data.text.split('\n') if 'heroStatsArr.concat' in line]
data=re.split(r"\(|\)",parsed_html[0])[1][1:-1]
players_tuple=ast.literal_eval(data)
for dic in players_tuple:
    print("-------------------------")
    print(f"team:{dic['teamName']}")
    print(f"player name:{dic['playerName']}")
    print(f"map : {dic['gameNumber']} -- {dic['map']}")
    print(f"hero :  {dic['hero']}")
    print(f"time played {int(dic['timePlayed']) // 60}:{int(dic['timePlayed'])% 60}")
