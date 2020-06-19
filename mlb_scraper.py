import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Initialise a DataFrame to be later filled with player data.
url = 'http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2019/start/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
header = soup.find('tr', attrs={'class':'colhead'})
columns = [col.get_text() for col in header.find_all('td')]

# Create a DataFrame with column names from above.
player_df = pd.DataFrame(columns=columns)

# For loop to iterate through each page of 50 players.
for i in range(1,301,50):
    # Extracting HTML source code from ESPN website.
    url = 'http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2019/start/'+str(i)

    # Create a BeautifulSoup of the source code and parse in HTML.
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Gather the player data from each row of the ESPN soup.
    players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})

    # For loop to interate through each player in the list of all players.
    for player in players:
        # Get the stats for each player.
        stats = [stat.get_text() for stat in player.find_all('td')]

        # Create a temp DataFrame for current player's stats.
        temp_df = pd.DataFrame(stats).transpose()
        temp_df.columns = columns

        # Concatenate temp_df with player_df
        player_df = pd.concat([player_df,temp_df], ignore_index=True)

player_df.to_csv(r"mls_stats.csv", index=False, sep=',', encoding='utf-8')
