import requests
from bs4 import BeautifulSoup
import time, sched
from datetime import datetime


url = 'https://www.margonem.pl/?task=stats' # URL's for Margonem's page where stats are

headers = {'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.3'
'(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.142'}

s = sched.scheduler(time.time, time.sleep) # Defining scheduler



def check_amount():
    now = datetime.now().strftime("%Y-%m-%d %H:%M") # Date exact up to minutes

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    world = 'Hypnos' # World name

    cut = len(world) + 19

    amount_online = soup.find(id="online_" + world).get_text() # online-<world_name> - for any world.
    tmp = str(amount_online[cut:]) # Cutting first row, for every world different length. Depends on length of name.
                                   # Also I'm not cutting "Zakończ" because it doesn't  affect my final result.
    temp = list(tmp.split(",")) # Making a list from string. Separator is a comma.
    #print(len(temp)) # List length of all players online. Printing is optional.

    f = open('online_' + world + '.csv', 'a+')  # Opennig/creating .csv file
    f.write( now + ',' + str(len(temp)) + '\n')
    f.close()


    s.enter(5,1,check_amount) # Function is executing every 300 seconds = 5 minutes.
                                # Data on the website updates every ~2 minutes so smaller amonut doesn't make sens. Can be longer though.

s.enter(5,1,check_amount)
s.run() # Running script
