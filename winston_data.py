
dps_players={
    "Ado":"WAS",
    "Adora":"HZS",
    "Agilities":"VAL",
    "aKm":"DAL",
    "Apply":"FLA",
    "Architect":"SFS",
    "Baconjack":"CDH",
    "Bazzi":"HZS",
    "BIRDRING":"LDN",
    "blase":"BOS",
    "bqb":"FLA",
    "carpe":"PHI",
    "ColourHex":"BOS",
    "Corey":"WAS",
    "dafran":"ATL",
    "Danteh":"HOU",
    "DDing":"SHD",
    "Decay":"GLA",
    "diem":" SHD",
    "EFFECT":"DAL",
    "Eileen":"GZC",
    "eqo":"PHI",
    "Erster":"ATL",
    "Fleta":"SEO",
    "GodsB":"HZS",
    "Guard":"LDN",
    "Haksal":"VAN",
    "Happy":"GZC",
    "Hydration":"GLA",
    "ivy":"TOR",
    "Jake":"HOU",
    "JinMu":"CDH",
    "KariV":"VAL",
    "KSF":"VAL",
    "Kyb":"GZC",
    "Libero":"NYE",
    "LiNkzr":"HOU",
    "Munchkin":"SEO",
    "Nenne":"NYE",
    "NiCOgdh":"PAR",
    "NLaaeR":"ATL",
    "Profit":"LDN",
    "Rascal":"SFS",
    "Saebyeolbe":"NYE",
    "sayaplayer":"FLA",
    "SeoMinSoo":"VAN",
    "sinatraa":"SFS",
    "snillo":"PHI",
    "SoOn":"PAR",
    "Stellar":"TOR",
    "Stitch":"VAN",
    "Stratus":"WAS",
    "STRIKER":"SFS",
    "Surefour":"GLA",
    "TviQ":"FLA",
    "YOUNGJIN":"SHD",
    "ZachaREEE":"DAL",
}

support_players={
    "Aid":"TOR",
    "AimGod":"BOS",
    "alemao":"BOS",
    "Anamo":"NYE",
    "ArK":"NYE",
    "Bani":"HOU",
    "Bdosin":"LDN",
    "BEBE":"HZS",
    "BigGoose":"GLA",
    "Boink":"HOU",
    "Boombox":"PHI",
    "Chara":"GZC",
    "Closer":"DAL",
    "CoMa":"SHD",
    "Custa":"VAL",
    "Dogman":"ATL",
    "Elk":"PHI",
    "Fahzix":"WAS",
    "Gido":"WAS",
    "HaGoPeun":"FLA",
    "Hyeonu":"WAS",
    "HyP":"PAR",
    "iDK":"HZS",
    "IZaYaKI":"VAL",
    "Jecse":"SEO",
    "JJONAK":"NYE",
    "Kellex":"BOS",
    "Kodak":"ATL",
    "Kris":"FLA",
    "Kruise":"PAR",
    "Kyo":"CDH",
    "Luffy":"SHD",
    "Masaa":"ATL",
    "moth":"SFS",
    "Neko":"TOR",
    "neptuNo":"PHI",
    "NUS":"LDN",
    "RAPEL":"VAN",
    "Rawkus":"HOU",
    "Revenge":"HZS",
    "RoKy":"TOR",
    "ryujehong":"SEO",
    "Shaz":"GLA",
    "shu":"GZC",
    "sleepy":"SFS",
    "SLIME":"VAN",
    "Twilight":"VAN",
    "uNKOE":"DAL",
    "Viol2t":"SFS",
    "Yveltal":"CDH",
}

tank_players={
    "ameng":"CDH",
    "Axxiom":"BOS",
    "BenBest":"PAR",
    "BUMPER":"VAN",
    "Choihyobin":"SFS",
    "coolmatt":"HOU",
    "Daco":"ATL",
    "Elsa":"CDH",
    "Envy":"TOR",
    "Fate":"VAL",
    "Finnsi":"PAR",
    "Fissure":"SEO",
    "Fury":"LDN",
    "Fusions":"BOS",
    "Gamsu":"SHD",
    "Gator":"ATL",
    "Geguri":"SHD",
    "Gesture":"LDN",
    "Guxue":"HZS",
    "HOTBA":"GZC",
    "Janus":"WAS",
    "JJANU":"VAN",
    "KuKi":"VAL",
    "lateyoung":"CDH",
    "Mano":"NYE",
    "Mcgravy":"FLA",
    "MekO":"NYE",
    "Michelle":"SEO",
    "Muma":"HOU",
    "Nevix":"SFS",
    "NoSmite":"HZS",
    "NotE":"BOS",
    "OGE":"DAL",
    "Poko":"PHI",
    "Pokpo":"ATL",
    "rCk":"DAL",
    "Ria":"HZS",
    "Rio":"GZC",
    "rOar":"GLA",
    "Sado":"PHI",
    "Sansam":"WAS",
    "Smurf":"SFS",
    "SPACE":"VAL",
    "SPREE":"HOU",
    "super":"SFS",
    "SWoN":"FLA",
    "Void":"GLA",
    "xepheR":"FLA",
    "Yakpung":"TOR",
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

"""
team_stats Parameters:
side = home or away ream
data = web scraped data
csv = file to write to
map = specific map data to print. 0 = print all maps
"""
def team_stats(side,data,csv,map=0):
    elems=soup.find_all("table",class_="table table-striped "+side+" sortable-table match")
    players = {}
    with open (csv,'a') as sheet:
        for i, el in enumerate(elems):
            if map == 0:
                if i == 0:
                    print("************************************************")
                    print("Match Stats:")
                    print("************************************************")
                else:
                    print("************************************************")
                    print("Map "+str(i)+" Stats:")
                    print("************************************************")
            else:
                if i == map:
                    print("************************************************")
                    print("Map " + str(i) + " Stats:")
                    print("************************************************")
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
                    if i == map or map == 0:
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

                        sheet.write(str(i)+","+str(players[player][5]) + "," + str(players[player][4])+","+str(players[player][0])+","+str(players[player][1])+","
                                    +str(players[player][2])+","+str(players[player][3]))
            sheet.write('\n')

def collect_match_data(data):
    csv = "winston_data.csv"
    team_stats("left-side", data, csv, 1)  # away team
    team_stats("right-side", data, csv, 1)  # home team
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