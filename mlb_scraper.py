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

# Create a DataFrame with column names from above
player_data = pd.DataFrame(columns=columns)
print(player_data)
