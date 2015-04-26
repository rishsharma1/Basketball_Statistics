import csv
import pdb
import math


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

#returns data for a player from a specific season
def get_player_season(data,player,season):

	return get_specific_data(get_specific_data(data,'Player',player),'Season',season)

#returns data for a team from a specific season 
def get_team_season(data,team,season):
	return get_specific_data(get_specific_data(data,'Tm',team),'Season',season)

#takes a list of numerical values
#returns standard deviation (population)
def get_std_dev(alist):

	float_list = [float(val) for val in alist if val != '']
	length = len(alist)
	total = sum(float_list);
	mean = float(total/length) if length != 0 else float('nan');
	dev = 0.0
	
	for val in float_list:
		dev += (val - mean) ** 2
	
	std_dev = math.sqrt(dev / length)
	
	return std_dev
		
#takes a range of years
#returns a dictionary containing the followings:
#1. std_dev: standard deviation
#2. ... (more can be added later)  
#3. ...
#calculation will be performed on the selected columns
def get_stats(data,begin,end):

	stats = {}
	sub_data = {} 
	#the following keys are not used for calculation 
	unwanted_keys = ['Rk', 'Player', 'Season', 'Year', 'Month', 'Age', 'Tm', 'Lg', '3P%']

	#subtract rows whose 'Year' is in the specified range 
	for year in range(begin, end+1):
		
		pos = get_index(data,'Year',str(year))
		#pos = get_index(data,'Age',str(year))

		if pos != []: 

			for year_row in pos:

				for key in data.keys():

					try:
						sub_data[key].append(data[key][year_row])
					except KeyError:
						sub_data[key] = [data[key][year_row]]

	#calculate stats
	for key in data.keys():

		if key not in unwanted_keys:

			row = sub_data[key]
			# some more stats calculations will be added here 
			std_dev = get_std_dev(row)
			stats.update({key: std_dev})

	return stats

def create_table(row,col,val=None):
    
    data = get_all_data('dataclean.csv')
    table_str = ''
    table_str += 'Content-Type: text/html\n'
    table_str += '<html><body><table border="1"><tr><td></td><td></td>'
    #we first need to print the header
    unique_row = list(set(data[row]))
    unique_col = list(set(data[col]))
    count = 0
    
    for item in unique_col:
        
        table_str += """<td>%s</td>"""%(item)
    
    
    for row_item in unique_row:
        
        table_str += """<tr><td>%d</td><td>%s</td>"""%(count,row_item)
        
        for col_item in unique_col:
            
            needed_data = get_specific_data(get_specific_data(data,row,row_item),col,col_item)
            
            if(needed_data):
                table_str += """<td>%d</td>"""%(sum(map(int,needed_data[val])))
            else:
                table_str += '<td></td>'
        count += 1
                
        table_str += '</tr>'
            
    table_str += '</tr></table></body></html>'
    
    open('output.html','w').write(table_str)


create_table('Player','Season','FG')



data = get_all_data('dataclean.csv')


#data = get_all_data('test.csv')

