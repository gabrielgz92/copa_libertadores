import requests
from bs4 import BeautifulSoup
import re
import csv
import itertools


years = list(range(1960, 2021))

# Iterate over the years and fetch data.
def url_generator_by_year(years):
    url = "https://www.livefutbol.com/jugador/copa-libertadores-{}/"
    year_urls_list = []
    for year in years:
      year_url = url.format(year)
      year_urls_list.append(year_url)
    return year_urls_list

# Fetch all the data iterating through all the url's by year.
def fetch_data(url_list):
    for each_url in url_list:
      results = requests.get(each_url)
      src = results.content
      soup = BeautifulSoup(src, "html.parser")
      tr = soup.find_all("tr")
      retrieve_team_info_block(tr)

# Get each one of the teams block of info.
def retrieve_team_info_block(tr):
    team_data_list = []
    master_data_list = []
    for each_block in tr:
      if len(each_block.find_all("td")) == 8:
        pass
        team_info_block = each_block.find_all("td")
        team = retrieve_team_info_lines(team_info_block)
        team_data_list.append(team)
        #Clean duplicates.
        # team_data_list = delete_duplicates(team_data_list)
    write_csv(team_data_list)

# Get each one of the lines of teams block info.
def retrieve_team_info_lines(td_block):
    team = []
    for each_line in td_block:
      if each_line.find('img') != None and each_line.find('img')['alt'] != "Página web oficial":
        team.append((each_line.find('img')['alt']))
    return team

# Write each team in a row
def write_csv(teams_data_list):
    with open('teams.csv', 'a', newline='') as file:
      writer = csv.writer(file, delimiter=',')
      writer.writerows(teams_data_list)

# Delete all the teams duplicated.
def delete_duplicates(list_of_lists):
    list_of_lists.sort()
    new_list = list(list_of_lists for list_of_lists,_ in itertools.groupby(list_of_lists))
    return new_list


# RUN THE CODE BABY
with open('teams.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["team", "country"])
fetch_data(url_generator_by_year(years))








