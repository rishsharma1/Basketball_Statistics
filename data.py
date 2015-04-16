import csv
import pdb


#will get all the data that is in 
#the csv file, some of this data may
#be used and may not be.
def get_all_data(input_file):

	
	csv_file = open(input_file) 
	data = csv.DictReader(csv_file)
	store = {}

	for row in data:

		for key in row.keys():
			
			try:
				store[key].append(row[key])
			except KeyError:
				store[key] = [row[key]] 

	return store


#this is used to get a list of indices of
#a given attribute and given item of that 
#attribute.
#Example: All the indices of where Kobe Bryant
#occurs, Key = 'Player', Query = 'Kobe Bryant'
def get_index(data,key,query):
	pos = []
	for val in range(len(data[key])):
		if data[key][val] == query:
			pos.append(val)
	return pos

#returns a dictionary of a given player's stats			
#throught 1999-2007
def get_player_data(data,player):

	player_info = {}

	#all the index positions of given player
	pos = get_index(data,'Player',player)

	for i in pos:

		for key in data.keys():

			try:
				player_info[key].append(data[key][i])
			except KeyError:
				player_info[key] = [data[key][i]]
	return player_info

#gets all data for a given season

def get_season_data(data,season):

	season_info = {}

	pos = get_index(data,'Season',season)

	for i in pos:


		for key in data.keys():

			try:
				season_info[key].append(data[key][i])
				
			except KeyError:
				season_info[key] = [data[key][i]]
			
	
	return season_info

data = get_all_data('dataclean.csv')







