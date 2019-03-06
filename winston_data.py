
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
    "BigG00se":"GLA",
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
damage = set(key.lower() for key in dps_players.keys())
support = set(key.lower() for key in support_players.keys())
tank = set(key.lower() for key in tank_players.keys())

import bs4
import requests

match_urls=["https://www.winstonslab.com/matches/match.php?id=40"+str(i) for i in range(58,110)]

#for match_rl in match_urls #once we know it works

match_url=match_urls[0]
html_data=requests.get(match_url)
html_data.raise_for_status()
soup= bs4.BeautifulSoup(html_data.text,features="lxml")
def team_stats(side):
    elems=soup.find_all("table",class_="table table-striped "+side+" sortable-table match")
    players = {}
    for i, el in enumerate(elems):
        if i == 0:
            print("************************************************")
            print("Match Stats:")
            print("************************************************")
        else:
            print("************************************************")
            print("Map "+str(i)+" Stats:")
            print("************************************************")
        names = el.find_all("a")
        killdeathratio = el.find_all("td", class_="center page1")
        kills = []
        deaths = []
        for index, kdr in enumerate(killdeathratio):
            if index % 2 == 0:
                kills.append(kdr)
            else:
                deaths.append(kdr)
        ults = el.find_all("td", class_="center page1 not-in-small")
        for index, name in enumerate(names):
            players[str(name.contents[0])] = [kills[index].contents, deaths[index].contents,
                                           ults[index].contents]
        for player in players:
            print("Name: " + str(player))
            if player.lower() in damage:
                print("Role: Damage")
            elif player.lower() in support:
                print("Role: Support")
            elif player.lower() in tank:
                print("Role: Tank")
            print("Kills: " + str(players[player][0][0]))
            print("Deaths: " + str(players[player][1][0]))
            print("Ults: " + str(players[player][2][0]))

if __name__ == '__main__':
    team_stats("left-side")
    team_stats("right-side")
