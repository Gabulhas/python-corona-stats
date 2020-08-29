import requests
from bs4 import BeautifulSoup

all_countries_stats = {}

page_code = requests.get("https://www.worldometers.info/coronavirus/").content

soup = BeautifulSoup(page_code, 'html.parser')
main_table = soup.select_one("table#main_table_countries_today")
table_headers = main_table.findChild("thead")

headers = []

"""
Fetches all the headers of the table like CountryName, New Deaths, etc
"""
for header in table_headers.findChildren("th"):
    headers.append(header.text.replace("\n", " ").strip())

name_index = headers.index("Country,Other")

"""
Gets the part of the table that contains the stats for each country
"""
all_countries = main_table.findChild("tbody")

"""
Iterates over every country Table Row
"""
for children in all_countries.findChildren("tr"):
    country_stats = children.findChildren("td")
    if country_stats[name_index].text is None:
        continue
    country_name = country_stats[name_index].text
    all_countries_stats[country_name] = {}
    """
    Iterates over every column in the row    
    """
    for stat_ind in range(0, len(headers)):
        stat_name = headers[stat_ind]
        stat_value = country_stats[stat_ind].text

        all_countries_stats[country_name][stat_name] = stat_value


def pretty_print(specific_stats):
    print("-----------------------------")
    for key in specific_stats:
        print(key + ": " + specific_stats[key])


for country_name in all_countries_stats:
    pretty_print(all_countries_stats[country_name])
