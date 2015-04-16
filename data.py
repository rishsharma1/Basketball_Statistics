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

#returns a dictionary of a specific targeted data
#this can be a specific season's data, or specific
#player stats etc.
def get_specific_data(data,att,query):

	specific_info = {}

	#all the index positions of given player
	pos = get_index(data,att,query)

	for i in pos:

		for key in data.keys():

			try:
				specific_info[key].append(data[key][i])
			except KeyError:
				specific_info[key] = [data[key][i]]
	return specific_info



data = get_all_data('dataclean.csv')
print get_specific_data(data,'Tm','LAL')['FG']






