import numpy as np
from bs4 import BeautifulSoup
import requests

player_list = []
url = 'https://www.fifaindex.com/players/{}/'   #creating url for primary pages



pageno = 400

while True:
    webpage = url.format(pageno)
    response1 = requests.get(webpage)
    if response1.status_code != 200:   # if maximum page exceeded, break out of loop
        break
    mainpage = response1.text
    mainsoup = BeautifulSoup(mainpage,'lxml')   # turn primary page into soup
    for tag in mainsoup.find_all('td',attrs={'data-title':'Name'}):   #iterate through each player on primary pages
        
        webpage2 = 'https://www.fifaindex.com'+str(tag.find('a')['href'])   #link for secondary pages
        response2 = requests.get(webpage2)
        subpage = response2.text
        soup = BeautifulSoup(subpage,'lxml')     # turn secondary page into soup
                                                   
        Player = soup.find_all('h5', class_='card-header')[0].contents[0]   
        Overall_Score = soup.find_all('h5', class_='card-header')[0].contents[1].contents[0].text  
        Potential_Score = soup.find_all('h5', class_='card-header')[0].contents[1].contents[-1].text    
        if soup.find_all('p', class_='data-currency data-currency-euro'):
            Market_Value = ''.join([i for i in soup.find_all('p', class_='data-currency data-currency-euro')[0].findNext().text if i.isdigit()])
            Weekly_Salary = ''.join([i for i in soup.find_all('p', class_='data-currency data-currency-euro')[1].findNext().text if i.isdigit()])
        else:
            Market_Value = np.nan
            Weekly_Salary = np.nan
        Height = soup.find_all('span', class_="data-units data-units-metric")[0].text.split()[0]   
        Weight = soup.find_all('span', class_="data-units data-units-metric")[1].text.split()[0]   
        Age = soup.find(text='Age ').findNext().text
        Preferred_Foot = soup.find(text='Preferred Foot ').findNext().text

        Ball_Control = float(soup.find(text='Ball Control ').findNext().text)
        Dribbling = float(soup.find(text='Dribbling ').findNext().text)
        Ball_Skills = np.mean([Ball_Control,Dribbling])

        Marking = float(soup.find(text='Marking ').findNext().text)
        Slide_Tackle = float(soup.find(text='Slide Tackle ').findNext().text)
        Stand_Tackle = float(soup.find(text='Stand Tackle ').findNext().text)
        Defence = np.mean([Marking,Slide_Tackle,Stand_Tackle])

        Aggression = float(soup.find(text='Aggression ').findNext().text)
        Reactions = float(soup.find(text='Reactions ').findNext().text)
        Attack_Position = float(soup.find(text='Att. Position ').findNext().text)
        Interceptions = float(soup.find(text='Interceptions ').findNext().text)
        Vision = float(soup.find(text='Vision ').findNext().text)
        Composure = float(soup.find(text='Composure ').findNext().text)
        Mental = np.mean([Aggression,Reactions,Attack_Position,Interceptions,Vision,Composure])

        Crossing = float(soup.find(text='Crossing ').findNext().text)
        Short_Pass = float(soup.find(text='Short Pass ').findNext().text)
        Long_Pass = float(soup.find(text='Long Pass ').findNext().text)
        Passing = np.mean([Crossing,Short_Pass,Long_Pass])

        Acceleration = float(soup.find(text='Acceleration ').findNext().text)
        Stamina = float(soup.find(text='Stamina ').findNext().text)
        Strength = float(soup.find(text='Strength ').findNext().text)
        Balance = float(soup.find(text='Balance ').findNext().text)
        Sprint_Speed = float(soup.find(text='Sprint Speed ').findNext().text)
        Agility = float(soup.find(text='Agility ').findNext().text)
        Jumping = float(soup.find(text='Jumping ').findNext().text)
        Physical = np.mean([Acceleration,Stamina,Strength,Balance,Sprint_Speed,Agility,Jumping])

        Heading = float(soup.find(text='Heading ').findNext().text)
        Shot_Power = float(soup.find(text='Shot Power ').findNext().text)
        Finishing = float(soup.find(text='Finishing ').findNext().text)
        Long_Shots = float(soup.find(text='Long Shots ').findNext().text)
        Curve = float(soup.find(text='Curve ').findNext().text)
        FK_Acc = float(soup.find(text='FK Acc. ').findNext().text)
        Penalties = float(soup.find(text='Penalties ').findNext().text)
        Volleys = float(soup.find(text='Volleys ').findNext().text)
        Shooting = np.mean([Heading,Shot_Power,Finishing,Long_Shots,Curve,FK_Acc,Penalties,Volleys])

        GK_Positioning = float(soup.find(text='GK Positioning ').findNext().text)
        GK_Diving = float(soup.find(text='GK Diving ').findNext().text)
        GK_Handling = float(soup.find(text='GK Handling ').findNext().text)
        GK_Kicking = float(soup.find(text='GK Kicking ').findNext().text)
        GK_Reflexes = float(soup.find(text='GK Reflexes ').findNext().text)
        Goalkeeping = np.mean([GK_Positioning,GK_Diving,GK_Handling,GK_Kicking,GK_Reflexes])


        player = {'Player':Player,'Overall Score':Overall_Score,'Potential Score':Potential_Score,'Market Value':Market_Value,
                 'Weekly Salary':Weekly_Salary,'Height':Height,'Weight':Weight,'Age':Age,'Preferred Foot':Preferred_Foot,
                'Ball Skills':Ball_Skills,'Defence':Defence,'Mental':Mental,'Passing':Passing,'Physical':Physical,'Shooting':Shooting,
                'Goalkeeping':Goalkeeping}                                                   
        player_list.append(player)    
    
    print(pageno)
    pageno += 1