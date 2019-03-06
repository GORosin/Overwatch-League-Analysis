import  bs4
import requests
print("************************************************")
print("IMAGINATION IS THE ESSENCE OF DISCOVERY")
print("************************************************")

match_urls=["https://www.winstonslab.com/matches/match.php?id=40"+str(i) for i in range(58,110)]

match_url=match_urls[0]
html_data=requests.get(match_url)
html_data.raise_for_status()
soup= bs4.BeautifulSoup(html_data.text,features="lxml")
rein_bar=0
winston_bar=0
sombra_bar=0
ana_bar=0
hammon_bar=0
mercy_bar=0
orisa_bar=0
#print(soup)
elems=soup.find_all("div",class_="progress-bar bar-hero bar-* bar-dataset1")
print(elems)

