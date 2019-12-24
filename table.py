from bs4 import BeautifulSoup
import requests
from texttable import Texttable

# Setting up the specific link to scrape
query_param = input("Please enter Pokemon name: ").lower()

# Setting up bs4 object for serebii.net
URL_serebii = "https://www.serebii.net/pokedex-swsh/" + query_param + '/'
serebii_page = requests.get(URL_serebii)
if serebii_page.status_code:
    soup = BeautifulSoup(serebii_page.content, 'html.parser')
else:
    print('Serebii page not found')

# Setting up bs4 object for pikalytics.com
URL_pikalytics = "https://pikalytics.com/pokedex/ss/" + query_param
pikalytics_page = requests.get(URL_pikalytics)
if pikalytics_page.status_code:
    soup2 = BeautifulSoup(pikalytics_page.text, 'html.parser')
else:
    print('Pikalytics page not found')


def create_table(header_list, data_list):
    '''
    This function creates a table of either two or three columns using 2D arrays of data passed in
    :param header_list: list, desired table header
    :param data_list: 2D list passed in to be the table data
    :return: no return, prints the table to the terminal
    '''
    table = Texttable()
    table.set_max_width(300)
    table.add_row(header_list)
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip().split(' ')
        if len(data_list[i]) == 5 or len(data_list[i]) == 4:
            data_list[i] = [(data_list[i][0] + ' ' + data_list[i][1]).rstrip(),
                            data_list[i][len(data_list[i]) - 2],
                            data_list[i][len(data_list[i]) - 1]
                            ]
        elif len(data_list[i]) == 3:
            data_list[i] = [data_list[i][0], data_list[i][1], data_list[i][2]]
        if len(header_list) == 2:
            table.add_row([(data_list[i][0] + ' ' + data_list[i][1]).rstrip(), data_list[i][len(data_list[i]) - 1]])
        else:
            table.add_row([data_list[i][0], data_list[i][1], data_list[i][2]])
    print(table.draw())


# Typing - works for multi-type Pokemon as well
typing = soup.find_all(class_='typeimg')
type = ''
for text in typing:
    type += text['alt'] + ' '


# Popularity Ranking - taken from Pikalytics
usage_percent = soup2.find(class_='pokemon-ind-summary-text gold-font').text
monthly_rank = soup2.find(class_='pokemon-ind-summary-text purple-font').text

# General Pokemon Information - Pkmn type, online usage rank, and probability of battling one online
general_info_table = Texttable()
str = '\n\t' + query_param.title()
print(str.expandtabs(16))
general_info_table.add_rows([['Typing', 'Usage Rank', 'Encounter Rate'], [type, monthly_rank, usage_percent]])
print(general_info_table.draw())

# Stats section
stats = soup.find_all(class_=['foohin', 'fooinfo', 'fooben'])
stats_list = []

for i in range(len(stats)):
    if 'Base Stats' in stats[i].text:
        while i < len(stats):
            stats_list.append(stats[i].text)
            i += 1
        break
    else:
        continue

# Formatting several data points for easier table use later
stats_list.insert(1, 'Lv. 0')
for i in range(8, len(stats_list), 16):
    temp = stats_list[i][:9] + ' ' + stats_list[i][9:len(stats_list[i])]
    stats_list[i] = temp
    stats_list.insert(i + 8, temp)

# Creating and formatting the stats table using the Texttable class
str = '\n\tBase Stats'
print(str.expandtabs(50))
stats_table = Texttable()
stats_table.set_max_width(200)
stats_table.add_row(['\t\t', 'Pkmn Lvl', 'HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed'])
for i in range(0, len(stats_list), 8):
    stats_table.add_row(stats_list[i:i+8])
print(stats_table.draw())

# Pikalytics data
# EV Spread Data
str = '\n\tCommon EV Spreads'
print(str.expandtabs(14))
ev_data = soup2.find(id='spread_wrapper').text.replace('\n', ' ').strip().split('   ')
print(create_table(['Nature', 'HP/Atk/Def/SpA/SpD/Spe', 'Popularity'], ev_data))

# Items Data
str = '\n\tCommon Items'
print(str.expandtabs(10))
item_data = soup2.find(id='items_wrapper').text.replace('\n', ' ').strip().split('     ')
print(create_table(['Item', 'Popularity'], item_data))

# Ability Data
str = '\n\tAbilities'
print(str.expandtabs(10))
ability_data = soup2.find(id='abilities_wrapper').text.replace('\n', ' ').strip().split('   ')
create_table(['Ability', 'Popularity'], ability_data)

# Move Data
str = '\n\tCommon Moves'
print(str.expandtabs(12))
move_data = soup2.find(id='moves_wrapper').text.replace('\n', ' ').strip().split('   ')
create_table(['Move', 'Move Type', 'Popularity'], move_data)

# Teammate Data
teammate_data = soup2.find(id='teammate_wrapper').text.replace('\n', ' ').strip().split('    ')
str = '\n\tCommon Teammates'
print(str.expandtabs(14))
create_table(['Pokemon', 'Typing', 'Popularity'], teammate_data)
