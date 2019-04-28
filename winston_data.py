import bs4
import requests
import re
import ast
import os
import time
import math
import pandas as pd
import pickle
from dictionaries import *

#format of data list of maps
#each maps has a dictionary of {map:map_name, player 1:[(hero,time),(hero,time)], player 2:[(hero,time),(hero,time)]...}
role_probs=pd.read_csv("hero_liklihood_matrix.txt")
role_probs=role_probs.set_index("hero")

#save data for debugging purposes
def save_html(request,filename):
    pickle.dump(request, open( filename, "wb" ))

def get_html(filename):
    return pickle.load( open(filename, "rb" ))

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
    heroes={'Reinhardt':0,'Winston':0,'Orisa':0,'Hammond':0,'Zarya':0,'D.Va':0,'Roadhog':0,'Widowmaker':0,"Tracer":0,"Sombra":0,"Pharah":0,"Other":0,"Brigitte":0,"Ana":0,"Zenyatta":0,"Mercy":0,"Lucio":0,"Moira":0,"Mccree":0,'Torbjörn':0}
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
            "Sombra_Goats":round(sombra_goats,3),
            "Savta_Goats":round(savta_goats,3),
            "Wrecking_Crew":round(wrecking_crew,3)}

def write_comp(team,data,csv):
    comp_data=hero_play_time(data,team)
    comp_dict=calculate_comp(comp_data)
    with open(csv,"a") as csv_file:
        csv_file.write(str(comp_dict['Goats'])+",")
        csv_file.write(str(comp_dict['Winston_Goats'])+",")
        csv_file.write(str(comp_dict['Sombra_Goats'])+",")
        csv_file.write(str(comp_dict['Savta_Goats'])+",")
        csv_file.write(str(comp_dict['Dive'])+",")
        csv_file.write(str(comp_dict['Wrecking_Crew']))

"""
team_stats Parameters:
side = home or away ream
data = web scraped data
csv = file to write to
map = specific map data to print. 0 = print all maps
"""
def team_stats(side, data, csv, game=0,write=True):
    elems=soup.find_all("table",class_="table table-striped "+side+" sortable-table match")
    players = [{},{},{},{},{},{}]
    team_name = ""
    with open (csv,'a') as sheet:
        for i, el in enumerate(elems):
            if i !=game:
                continue
            if game == 0:
                if i == 0:
                    print("************************************************")
                    print("Match Stats:")
                    print("************************************************")
                else:
                    print("************************************************")
                    print("Map "+str(i)+" Stats:")
                    print("************************************************")
            else:
                if i == game:
                    print("************************************************")
                    print("Map " + str(i) + " Stats:")
                    print("************************************************")
            names = el.find_all("a")
            killdeathratio = el.find_all("td", class_="center page1")
            kills = []
            deaths = []
            kdd = el.find_all("td", class_=re.compile("center page1 k-d-diff.* not-in-small"))

            for index, kdr in enumerate(killdeathratio):
                if index % 2 == 0:
                    kills.append(kdr)
                else:
                    deaths.append(kdr)
            ults = el.find_all("td", class_="center page1 not-in-small")

            

            player_data={}
            for index, name in enumerate(names):
                try:
                    player_data[name.contents[0]]={"Name":name.contents[0],
                                                   "stats": [kills[index].contents[0], deaths[index].contents[0],
                                                             ults[index].contents[0], kdd[index].contents[0].strip()],
                                                   "role":calculate_role_probabilities(data[name.contents[0]])}
                except Exception as e:
                    print(e)
                    player_data[name.contents[0].lower()]={"Name":name.contents[0].lower(),
                                                   "stats": [kills[index].contents[0], deaths[index].contents[0],
                                                             ults[index].contents[0], kdd[index].contents[0].strip()],
                                                   "role":default_role_probabilities(name.contents[0].lower())}
  
                
        players[0]=player_data[determine_player_role(player_data,'main_dps')]
        players[1]=player_data[determine_player_role(player_data,'flex_dps')]
        players[2]=player_data[determine_player_role(player_data,'main_tank')]
        players[3]=player_data[determine_player_role(player_data,'flex_tank')]
        players[4]=player_data[determine_player_role(player_data,'main_support')]
        players[5]=player_data[determine_player_role(player_data,'flex_support')]
        team_name=all_players[players[0]['Name'].lower()]
        for player in range(len(players)):
            print("Name: " + str(players[player]['Name']))
            print("Kills: " + str(players[player]['stats'][0]))
            print("Deaths: " + str(players[player]['stats'][1]))
            print("Ults: " + str(players[player]['stats'][2]))
            print("First Kills - Deaths: "+ str(players[player]['stats'][3]))
            print(team_name)
            if(write):
                sheet.write(str(players[player]['stats'][0])+","+str(players[player]['stats'][1])+","+
                            str(players[player]['stats'][2])+","+str(players[player]['stats'][3])+",")
    return team_name

def collect_match_data(data):
    csv = "winston_data.csv"
    if (not os.path.exists(csv)):
        with open(csv,"a") as sheet:
            sheet.write("away_team,home_team,map,")
            
            sheet.write("away_main_dps_kills,away_main_dps_deaths,away_main_dps_ults,away_main_dps_kdr,")
            sheet.write("away_flex_dps_kills,away_flex_dps_deaths,away_flex_dps_ults,away_flex_dps_kdr,")
            sheet.write("away_main_support_kills,away_main_support_deaths,away_main_support_ults,away_main_support_kdr,")
            sheet.write("away_flex_support_kills,away_flex_support_deaths,away_flex_support_ults,away_flex_support_kdr,")
            sheet.write("away_main_tank_kills,away_main_tank_deaths,away_main_tank_ults,away_main_tank_kdr,")
            sheet.write("away_flex_tank_kills,away_flex_tank_deaths,away_flex_tank_ults,away_flex_tank_kdr,")
            
            sheet.write("home_main_dps_kills,hom_main_dps_deaths,hom_main_dps_ults,hom_main_dps_kdr,")
            sheet.write("home_flex_dps_kills,hom_flex_dps_deaths,hom_flex_dps_ults,hom_flex_dps_kdr,")
            sheet.write("home_main_support_kills,hom_main_support_deaths,hom_main_support_ults,hom_main_support_kdr,")
            sheet.write("home_flex_support_kills,hom_flex_support_deaths,hom_flex_support_ults,hom_flex_support_kdr,")
            sheet.write("home_main_tank_kills,hom_main_tank_deaths,hom_main_tank_ults,hom_main_tank_kdr,")
            sheet.write("home_flex_tank_kills,hom_flex_tank_deaths,hom_flex_tank_ults,hom_flex_tank_kdr,")
            
            sheet.write("away_team_goats,away_team_Winston_goats,away_team_sombra_goats,away_team_ana_goats,away_team_dive,away_team_wrecking_crew,")
            sheet.write("home_team_goats,home_team_Winston_goats,home_team_sombra_goats,home_team_ana_goats,home_team_dive,home_team_wrecking_crew\n")
            
    home_team=''
    home_team=''
    for i in range(6):
        if i==0:
            away_team=team_stats("left-side", data[0], csv, i,False)  # away team
            home_team=team_stats("right-side", data[0], csv, i,False)  # home team
        else:
            try:
                away_team=team_stats("left-side", data[i-1], csv, i,False)  # away team
                home_team=team_stats("right-side", data[i-1], csv, i,False)  # home team
                away_team=away_team.strip()
                home_team=home_team.strip()
                with open(csv,"a") as sheet:
                    sheet.write(away_team)
                    sheet.write(",")
                    sheet.write(home_team)
                    sheet.write(",")
                    sheet.write(str(i)+",")
                team_stats("left-side", data[i-1], csv, i)  # away team
                team_stats("right-side", data[i-1], csv, i)  # home team
                write_comp(away_team,data[i-1],csv)
                with open(csv, 'a') as sheet:
                    sheet.write(",")
                write_comp(home_team,data[i-1],csv)
                with open(csv, 'a') as sheet:
                    sheet.write('\n')
                time.sleep(0.01)
            except Exception as e:
                print(e)
                print("no map 5")
                


def calculate_role_probabilities(hero_list):
    role_liklihoods={"main_dps":-1,"flex_dps":-1,"main_tank":-1,"flex_tank":-1,"main_support":-1,"flex_support":-1}
    for key,value in role_liklihoods.items():
        for hero in hero_list:
            role_liklihoods[key]+=math.log(role_probs.loc[hero[0],key]/100,2)+math.log(hero[1],2)
    return role_liklihoods

def default_role_probabilities(player):
    if player in damage_lower:
         return {"main_dps":0,"flex_dps":-1,"main_tank":-1,"flex_tank":-1,"main_support":-1,"flex_support":-1}
    if player in flex_damage_lower:
         return {"main_dps":-1,"flex_dps":0,"main_tank":-1,"flex_tank":-1,"main_support":-1,"flex_support":-1}
    if player in tank_lower:
         return {"main_dps":-1,"flex_dps":-1,"main_tank":0,"flex_tank":-1,"main_support":-1,"flex_support":-1}
    if player in flex_tank_lower:
         return {"main_dps":-1,"flex_dps":-1,"main_tank":-1,"flex_tank":0,"main_support":-1,"flex_support":-1}
    if player in support_lower:
         return {"main_dps":-1,"flex_dps":-1,"main_tank":-1,"flex_tank":-1,"main_support":0,"flex_support":-1}
    if player in flex_support_lower:
         return {"main_dps":-1,"flex_dps":-1,"main_tank":-1,"flex_tank":-1,"main_support":-1,"flex_support":0}

def determine_player_role(player_data,role):
    largest=-100
    role_player=''
    for player,data in player_data.items():
        if largest<data['role'][role]:
            largest=data['role'][role]
            role_player=player
    return role_player

def download_html():
    #match_urls = ["https://www.winstonslab.com/matches/match.php?id=" + str(4000+i) for i in range(58, 128)]
    match_urls = ["https://www.winstonslab.com/matches/match.php?id=" + str(4000+i) for i in range(58+16, 58+18)]
    for i,match_url in enumerate(match_urls):
        print("downloading: "+str(match_url))
        html_data = requests.get(match_url)
        html_data.raise_for_status()
        print("saving to "+"html_match_data/match_"+str(i)+".pkl")
        save_html(html_data,"html_match_data/match_"+str(i)+".pkl")
        
if __name__ == '__main__':
    print("************************************************")
    print("IMAGINATION IS THE ESSENCE OF DISCOVERY")
    print("************************************************")
    download_html()
    '''
    files=os.listdir("html_match_data")
    files.sort(key=lambda x:int(x.split("_")[-1].split(".")[0]))
    for html in files:
        html_data=get_html("html_match_data/"+html)
        soup = bs4.BeautifulSoup(html_data.text, features="lxml")
        parsed_html = [line for line in html_data.text.split('\n') if 'heroStatsArr.concat' in line]
        try:
            data = re.split(r"\(|\)", parsed_html[0])[1][1:-1]
        except Exception as e:
            with open("winstons_log.txt","a") as log:
                log.write("failed on: ")
                log.write(html)
                log.write(" because: ")
                log.write(str(e))
                log.write("\n")
            continue
        players_tuple = ast.literal_eval(data)
        sorted_data= sort_winstons_data(players_tuple)
        #csv="test.csv"
        #away_team=team_stats("left-side", sorted_data[4], csv, 4,False)
        #away_team=team_stats("right-side", sorted_data[2], csv, 1,False)
        
        #hero_times=hero_play_time(sorted_data[1],'LDN')
        #print(calculate_comp(hero_times))
    
        collect_match_data(sorted_data)
    '''
