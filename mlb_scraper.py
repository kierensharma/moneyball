import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Extracting HTML source code from ESPN website.
url = "http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2019"

# Create a BeautifulSoup of the source code and parse in HTML.
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# Extract the column names from the soup.
header = soup.find('tr', attrs={'class':'colhead'})
columns = [col.get_text() for col in header.find_all('td')]

# Create a DataFrame with column names from above.
player_df = pd.DataFrame(columns=columns)

# Gather the player data from each row of the ESPN table.
players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
for player in players:
    # Get the stats for each player.
    stats = [stats.get_text() for stat in player.find_all('td')]

    # Create a temp DataFrame for current player's stats.
    temp_df = pd.DataFrame(stats).transpose()
    temp_df.columns = columns

    # Concatenate temp_df with player_df
    player_df = pd.concat([player_df,temp_df], ignore_index=True)
