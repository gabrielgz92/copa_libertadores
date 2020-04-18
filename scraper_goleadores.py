import requests
from bs4 import BeautifulSoup
import re
import csv

years = list(range(1960, 2020))

# Iterate over the years and fetch data.
def url_generator_by_year(years):
    url = "https://www.livefutbol.com/goleadores/copa-libertadores-{}/"
    year_urls_list = []
    for year in years:
      year_url = url.format(year)
      year_urls_list.append(year_url)
    return year_urls_list

# Fetch all the data iterating through all the url's by year.
def fetch_data(url_list):
    for each_url in url_list:
      #Get the data.
      results = requests.get(each_url)
      src = results.content
      soup = BeautifulSoup(src, "html.parser")
      tr = soup.find_all("tr")
      #Retrieve the year again to then paste it in csv file.
      year = re.sub(r'\D+', "",each_url)
      #Call next function.
      retrieve_player_info_block(tr, year)

# Get each one of the players block of info.
def retrieve_player_info_block(tr, year):
  players_data_list = []
  for each_block in tr:
    if len(each_block.find_all("td")) == 6:
      pass
      player_info_block = each_block.find_all("td")
      player = retrieve_player_info_lines(player_info_block)
      player.append(year)
      players_data_list.append(player)
  write_csv(players_data_list)

# Get each one of the lines of player block info.
def retrieve_player_info_lines(td_block):
    player = []
    for each_line in td_block:
      string = each_line.text
      player.append(string.strip())
    del player[0]
    del player[1]
    player[-1] = clean_penalties(player[-1])
    return player

# Cleans the penalties
def clean_penalties(string):
    goals = re.sub(r'\((.*?)\)', "" ,string)
    return goals

# Write each player in a row
def write_csv(players_data_list):
  with open('goleadores.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(players_data_list)

# RUN THE CODE BABY
with open('goleadores.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["player_name", "country", "team","goals","year"])
fetch_data(url_generator_by_year(years))
