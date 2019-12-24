import requests
from bs4 import BeautifulSoup
from CSV import CSV
import os


def get_data(tag, num_spaces=1):
    """
    Creates 2D list by restructuring the data to remove excess newlines and set up the preliminary data to be then
    restructured further
    :param tag: html tag
    :param num_spaces: number of spaces to split the data by
    :return: 2D array of strings
    """
    data_list = tag.text.replace('\n', ' ').strip().split(' ' * num_spaces)
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip().split(' ')
        temp = []
        for j in range(len(data_list[i])):
            if data_list[i][j] != '':
                temp.append(data_list[i][j])
        data_list[i] = temp
    return data_list


def format_data(element_tag, desired_length=2, num_spaces=1, start_index=0, end_index=0):
    """
    Sets up a 2D lists of strings taken from an html tag
    Combines strings into a single string using a start and end index
    :param element_tag: tag resulted from using the find method on a soup object (html tag)
    :param desired_length: desired length of the data list
    :param num_spaces: number of spaces used to initially separate the data into separate lists - default 1
    :param start_index: index of list to start combining - default 0
    :param end_index: index of list to end combining - default 0
    :return: 2D list of strings
    """
    prelim_data = get_data(element_tag, num_spaces)
    for i in range(len(prelim_data)):
        if (desired_length == 3 and (len(prelim_data[i]) > 3)) or (desired_length == 2 and (len(prelim_data[i]) > 2)):
            temp_str = prelim_data[i][start_index] + ' ' + prelim_data[i][end_index]
            del (prelim_data[i][:2])
            prelim_data[i].insert(0, temp_str)
        elif (desired_length == 3) and ((len(prelim_data[i])) < 3):
            prelim_data[i].insert(1, ' ')
    return prelim_data


# Setting up bs4 object for pikalytics.com
# Checks to see if the link in question exists
URL_pikalytics = "https://pikalytics.com/pokedex/ss/"
pikalytics_page = requests.get(URL_pikalytics)
if pikalytics_page.status_code:
    soup = BeautifulSoup(pikalytics_page.text, 'html.parser')
else:
    print('Pikalytics page not found')

# Used for looking through the data and create the csv files
id_dict = {
    'moves_wrapper': [3, 3, 0, 1, ['Moves', 'Move', 'Type', 'Use Percentage']],
    'teammate_wrapper': [3, 4, 0, 0, ['Teammates', 'Pokemon', 'Type', 'Use Percentage']],
    'items_wrapper': [2, 5, 0, 1, ['Items', 'Item', 'Use Percentage']],
    'abilities_wrapper': [2, 3, 0, 1, ['Abilities', 'Ability', 'Use Percentage']],
    'spread_wrapper': [3, 3, 0, 0, ['EVs', 'Nature', 'HP/Atk/Def/SpA/SpD/Spe', 'Use Percentage']]
}

# Grabbing most used Pokemon online ranked 1 - 25 according to Pikalytics
most_popular = format_data(soup.find(id='min_list'), num_spaces=2)
for i in range(int(len(most_popular)/2)):
    temp_list = [most_popular[i][0], most_popular[i + 1][0]]
    most_popular[i] = temp_list
    del (most_popular[i + 1])

# Path needs to be specified by the user
path = ''

# For each Pokemon in the top 25, creates a CSV file for common moves, teammates, items, abilities, and ev spreads
# Checks to make sure the directories exist, and create new ones if they don't
for i in range(len(most_popular)):
    directory = path + most_popular[i][0].title()
    for key, value in id_dict.items():
        URL_pikalytics = "https://pikalytics.com/pokedex/ss/" + most_popular[i][0].lower()
        pikalytics_page = requests.get(URL_pikalytics)
        soup = BeautifulSoup(pikalytics_page.text, 'html.parser')
        data = format_data(soup.find(id=key), value[0], value[1], value[2], value[3])
        filepath = directory + '/' + most_popular[i][0] + '_' + value[4][0] + '.csv'
        file = CSV(data, filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            if not os.path.exists(filepath):
                file.create_file(value[4][1:len(value[4])])
        file.csv_write()

