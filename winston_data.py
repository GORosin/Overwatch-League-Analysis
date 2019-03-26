
dps_players={
    "Ado":"WAS",
    "Adora":"HZS",
    "Agilities":"VAL",
    "Apply":"FLA",
    "Architect":"SFS",
    "Bazzi":"HZS",
    "blase":"BOS",
    "DDing":"SHD",
    "Eileen":"GZC",
    "eqo":"PHI",
    "Erster":"ATL",
    "Guard":"LDN",
    "Haksal":"VAN",
    "Hydration":"GLA",
    "Jake":"HOU",
    "JinMu":"CDH",
    "KSF":"VAL",
    "Kyb":"GZC",
    "Libero":"NYE",
    "Munchkin":"SEO",
    "NiCOgdh":"PAR",
    "Rascal":"SFS",
    "snillo":"PHI",
    "Stellar":"TOR",
    "Stratus":"WAS",
    "TviQ":"FLA",
    "YOUNGJIN":"SHD",
    "ZachaREEE":"DAL",
}

main_dps={
    "aKm":"DAL",
    "Baconjack":"CDH",
    "BIRDRING": "LDN",
    "bqb": "FLA",
    "carpe": "PHI",
    "ColourHex": "BOS",
    "Corey": "WAS",
    "dafran": "ATL",
    "Danteh": "HOU",
    "Decay": "GLA",
    "diem": " SHD",
    "EFFECT": "DAL",
    "Fleta": "SEO",
    "GodsB": "HZS",
    "Happy": "GZC",
    "ivy": "TOR",
    "KariV": "VAL",
    "LiNkzr": "HOU",
    "Nenne": "NYE",
    "NLaaeR": "ATL",
    "Profit": "LDN",
    "Saebyeolbe": "NYE",
    "sayaplayer": "FLA",
    "SeoMinSoo": "VAN",
    "sinatraa": "SFS",
    "SoOn": "PAR",
    "Stitch": "VAN",
    "STRIKER": "SFS",
    "Surefour": "GLA",
}

support_players={
    "AimGod":"BOS",
    "Bdosin":"LDN",
    "BEBE":"HZS",
    "Boombox":"PHI",
    "Dogman":"ATL",
    "Gido":"WAS",
    "HaGoPeun":"FLA",
    "HyP":"PAR",
    "IZaYaKI":"VAL",
    "JJONAK":"NYE",
    "Kodak":"ATL",
    "Kyo":"CDH",
    "Luffy":"SHD",
    "Neko":"TOR",
    "RAPEL":"VAN",
    "Rawkus":"HOU",
    "Revenge":"HZS",
    "ryujehong":"SEO",
    "Shaz":"GLA",
    "shu":"GZC",
    "sleepy":"SFS",
    "Twilight":"VAN",
    "uNKOE":"DAL",
    "Viol2t":"SFS",
}

main_supports={
    "Aid":"TOR",
    "alemao":"BOS",
    "Anamo":"NYE",
    "ArK":"NYE",
    "Bani":"HOU",
    "BigGoose":"GLA",
    "Boink":"HOU",
    "Chara": "GZC",
    "Closer": "DAL",
    "CoMa": "SHD",
    "Custa": "VAL",
    "Elk": "PHI",
    "Fahzix": "WAS",
    "Hyeonu": "WAS",
    "iDK": "HZS",
    "Jecse": "SEO",
    "Kellex": "BOS",
    "Kris": "FLA",
    "Kruise": "PAR",
    "Masaa": "ATL",
    "moth": "SFS",
    "neptuNo": "PHI",
    "NUS": "LDN",
    "RoKy": "TOR",
    "SLIME": "VAN",
    "Yveltal": "CDH",
}

tank_players={
    "Choihyobin":"SFS",
    "coolmatt":"HOU",
    "Daco":"ATL",
    "Elsa":"CDH",
    "Envy":"TOR",
    "Finnsi":"PAR",
    "Fury":"LDN",
    "Geguri":"SHD",
    "HOTBA":"GZC",
    "JJANU":"VAN",
    "lateyoung":"CDH",
    "Mcgravy":"FLA",
    "MekO":"NYE",
    "Michelle":"SEO",
    "Nevix":"SFS",
    "NotE":"BOS",
    "Poko":"PHI",
    "rCk":"DAL",
    "Ria":"HZS",
    "Sansam":"WAS",
    "SPACE":"VAL",
    "SPREE":"HOU",
    "Void":"GLA",
    "xepheR":"FLA",
}

main_tanks={
    "ameng": "CDH",
    "Axxiom": "BOS",
    "BenBest": "PAR",
    "BUMPER": "VAN",
    "Fate": "VAL",
    "Fissure": "SEO",
    "Fusions": "BOS",
    "Gamsu": "SHD",
    "Gator": "ATL",
    "Gesture": "LDN",
    "Guxue": "HZS",
    "Janus": "WAS",
    "KuKi": "VAL",
    "Mano": "NYE",
    "Muma": "HOU",
    "NoSmite": "HZS",
    "OGE": "DAL",
    "Pokpo": "ATL",
    "Rio": "GZC",
    "rOar": "GLA",
    "Sado": "PHI",
    "Smurf": "SFS",
    "super": "SFS",
    "SWoN": "FLA",
    "Yakpung": "TOR",
}

#lower case versions of dictionaries for key searching
damage = dict((key.lower(),value) for key,value in dps_players.items())
support = dict((key.lower(),value) for key,value in support_players.items())
tank = dict((key.lower(),value) for key,value in tank_players.items())
all_players={**damage,**support,**tank}

import bs4
import requests
import re
import json
import ast

#format of data list of maps
#each maps has a dictionary of {map:map_name, player 1:[(hero,time),(hero,time)], player 2:[(hero,time),(hero,time)]...}

def sort_winstons_data(players_tuple):
    match_rounds=[{},{},{},{},{}]
    for dic in players_tuple:
        this_round=int(dic['gameNumber'])
        match_rounds[this_round-1]['map']=str(dic['map'])
        if dic['playerName'] in match_rounds[this_round-1]:
            match_rounds[this_round-1][dic['playerName']].append((str(dic['hero']),int(dic['timePlayed'])))
        else:
            match_rounds[this_round-1][dic['playerName']]=[(str(dic['hero']),int(dic['timePlayed']))]

    return match_rounds

def hero_play_time(round_data,team):
    heroes={'Reinhardt':0,'Winston':0,'Orisa':0,'Hammond':0,'Zarya':0,'D.Va':0,'Roadhog':0,'Widowmaker':0,"Tracer":0,"Sombra":0,"Pharah":0,"Other":0,"Brigitte":0,"Ana":0,"Zenyatta":0,"Mercy":0,"Lucio":0,"Moira":0,"Mccree":0,"Other":0}
    total_time=0
    for player,hero_list in round_data.items():
        if player=='map':
            continue
        if all_players[player.lower()]!=team:
            continue
        for hero in hero_list:
            if hero[0] not in heroes:
                heroes['Other']=+hero[1]
            else:
                heroes[hero[0]]+=hero[1]
            total_time+=hero[1]

    total_time=total_time/6.0
    heroes = dict((k, round(v/total_time,4)) for k, v in heroes.items())
    return heroes

def calculate_comp(hero_times):
    three_three=hero_times['Zarya']
    goats=hero_times['Reinhardt']
    winston_goats=three_three-goats-hero_times['Orisa']
    dive=hero_times['Winston']-winston_goats
    sombra_goats=hero_times['Zarya']-hero_times['D.Va'] if hero_times['Zarya']>hero_times['D.Va'] else 0
    savta_goats=hero_times['Zarya']-hero_times['Brigitte'] if hero_times['Zarya']>hero_times['Brigitte'] else 0
    #I wasn't cut out for retirement anyways.	
    total_dps=(hero_times['Widowmaker']+hero_times['Tracer'])/2
    wrecking_crew=total_dps-dive
    return {"Dive":round(dive,3),
            "Goats":round(goats,3),
            "Winston_Goats":round(winston_goats,3),
            "Sombra Goats":round(sombra_goats,3),
            "Savta Goats":round(savta_goats,3),
            "Wrecking_Crew":round(wrecking_crew,3)}

def team_stats(side,data,csv):
    elems=soup.find_all("table",class_="table table-striped "+side+" sortable-table match")
    players = {}
    with open (csv,'a') as sheet:
        for i, el in enumerate(elems):
            '''
            if i == 0:
                print("************************************************")
                print("Match Stats:")
                print("************************************************")
            else:
                print("************************************************")
                print("Map "+str(i)+" Stats:")
                print("************************************************")
            '''
            names = el.find_all("a")
            killdeathratio = el.find_all("td", class_="center page1")
            kills = []
            deaths = []
            kdd = el.find_all("td", class_=re.compile("center page1 k-d-diff.* not-in-small"))
            #for k in kdd:
             #   print(k.contents[0].strip())
            for index, kdr in enumerate(killdeathratio):
                if index % 2 == 0:
                    kills.append(kdr)
                else:
                    deaths.append(kdr)
            ults = el.find_all("td", class_="center page1 not-in-small")
            for index, name in enumerate(names):
                if str(name.contents[0]).lower() in damage:
                    players[str(name.contents[0])] = [kills[index].contents[0], deaths[index].contents[0],
                                                      ults[index].contents[0], kdd[index].contents[0].strip(),"Damage",damage[str(name.contents[0]).lower()]]
                    #print("Role: Damage")
                elif str(name.contents[0]).lower() in support:
                    players[str(name.contents[0])] = [kills[index].contents[0], deaths[index].contents[0],
                                                      ults[index].contents[0], kdd[index].contents[0].strip(), "Support",support[str(name.contents[0]).lower()]]
                    #print("Role: Support")
                elif str(name.contents[0]).lower() in tank:
                    players[str(name.contents[0])] = [kills[index].contents[0], deaths[index].contents[0],
                                                      ults[index].contents[0], kdd[index].contents[0].strip(), "Tank",tank[str(name.contents[0]).lower()]]
                    #print("Role: Tank")
            for player in players:
                if player in data[i-1] or i == 0 :
                    '''
                    print("Name: " + str(player))
                    if player.lower() in damage:
                        print("Role: Damage")
                    elif player.lower() in support:
                        print("Role: Support")
                    elif player.lower() in tank:
                        print("Role: Tank")
                    print("Kills: " + str(players[player][0]))
                    print("Deaths: " + str(players[player][1]))
                    print("Ults: " + str(players[player][2]))
                    print("First Kills - Deaths: "+ str(players[player][3]))
                    '''
                    sheet.write(str(i)+","+str(players[player][5]) + "," + str(players[player][4])+","+str(players[player][0])+","+str(players[player][1])+","
                                +str(players[player][2])+","+str(players[player][3])+",")
            sheet.write('\n')

def round_map_data(data):
    for round_map in data:
        if not round_map:
            break

        print('map ' + str(round_map['map']))
        print('my man ' + str(round_map['Eqo']))

def collect_match_data(data):
    csv = "winston_data.csv"
    team_stats("left-side", data, csv)  # away team
    team_stats("right-side", data, csv)  # home team
    with open(csv, 'a') as sheet:
        sheet.write('\n')

if __name__ == '__main__':
    print("************************************************")
    print("IMAGINATION IS THE ESSENCE OF DISCOVERY")
    print("************************************************")



    match_urls = ["https://www.winstonslab.com/matches/match.php?id=40" + str(i) for i in range(58, 110)]
    match_url=match_urls[0]
    html_data = requests.get(match_url)
    html_data.raise_for_status()
    soup = bs4.BeautifulSoup(html_data.text, features="lxml")
    parsed_html = [line for line in html_data.text.split('\n') if 'heroStatsArr.concat' in line]
    data = re.split(r"\(|\)", parsed_html[0])[1][1:-1]
    players_tuple = ast.literal_eval(data)
    sorted_data= sort_winstons_data(players_tuple)

    #hero_times=hero_play_time(sorted_data[2],'LDN')
    #print(calculate_comp(hero_times))
    #get_comp(players_tuple)
    collect_match_data(sorted_data)