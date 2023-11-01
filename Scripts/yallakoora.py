"""
This script was made to retreive data from yallakoora website
The data is : matches of the day , date ,score...
"""
import os
import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
date = input("Enter Date in the form of mm/dd/yyyy: ")
try :
    page = requests.get(f'https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#')
    page.raise_for_status()
except requests.exceptions.ConnectionError:
    print("Connection Error Occured")

except requests.exceptions.RequestException as e:
    print('An Error Occured!',e)

finally:
    ... #code cleanup    

data =[]

def main(page):
    src = page.content # get the src code of the page
    soup = BeautifulSoup(src ,'lxml') # making it readable
    championships = soup.find_all('div' , {'class': 'matchCard'}) # get All the championships of the day ex :UEFA/CAN/CAF... 
    def get_data(championships):        
        # In This loop: each time the loop goes with one championship card and gets the appropriate data => all the matches in this championship
        # there are two children inside the matchCard div, which are: .title and <ul>, we need title and .contents stores the children of the element as a list
        for i in range(len(championships)):
            # it normally should be contents[0], but there is a hidden element of type int before
            championship_title = championships[i].contents[1].find('h2').text.strip() # get the championship title
            all_matches = championships[i].contents[3].find_all('li') # all matches of one championship "(one card)")
            # get teams : This loop iterates through each match within one single championship
            for j in range(len(all_matches)):
                team_A = all_matches[j].find('div',{'class':'teamA'}).text.strip()  # get the team from the <ul> child =>championship[2]
                team_B = all_matches[j].find('div',{'class':'teamB'}).text.strip()  # ...
            # get the score  .matchCard =>ul =>li =>.allData =>teamCntnr =>.teamsData =>.MResult
            # This gives me a list of scores composed of this: [<span class="score">3</span>, <span class="score">2</span>]
                match_result = all_matches[j].find('div',{'class':'MResult'}).find_all('span',{'class' : 'score'}) 
                score = f"{match_result[0].text.strip()}-{match_result[1].text.strip()}"
            # get the time
                time = all_matches[j].find('div',{'class' : 'MResult'}).find('span',{'class' : 'time'}).text.strip()
                # print(time)
                data.append({'Championship' :championship_title , 'Team 1':team_A ,'Team 2':team_B ,'Match Time' :time, 'Match Date':date ,'Score' : score })
    get_data(championships)
main(page)
# Import data to csv file :
keys = data[0].keys()
# with open(rf"{os.getcwd()}/Projects/WebScraping/matches.csv",'w') as output_file:
#     dict_writer = csv.DictWriter(output_file,keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(data)

# Import data to DataBase :
db = sqlite3.connect('matches.db')
cr = db.cursor()
cr.execute(f"create table if not exists matches('{list(keys)[0]}' TXT , '{list(keys)[1]}' TXT , '{list(keys)[2]}' TXT ,'{list(keys)[3]}' NUM , '{list(keys)[4]}' NUM , '{list(keys)[5]}' NUM)") 
lst_length = len(data) 
for i in range(lst_length):
    values = list(data[i].values())
    cr.execute(f"insert into matches values('{values[0]}' , '{values[1]}' , '{values[2]}' , '{values[3]}' , '{values[4]}' , '{values[5]}' )")
    db.commit()
db.close()

"""
why not # lst = a.contents ; print(lst[i])#  but  # a.content[i];# ???
"""