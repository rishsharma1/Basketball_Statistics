import csv
from collections import defaultdict

SEASON_LENGTH = 81
MAX_AST_PG = 10
ASSISTS_INTERVAL = 1
AGE_INTERVAL = 5
WS_INTERVAL = 2
PTS_INTERVAL = 5
EFG_INTERVAL = 0.1
BLK_INTERVAL = 0.5
STL_INTERVAL = 0.5
TOV_INTERVAL = 0.5 




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

#returns unique row or column keys 
def create_keys(data, item):
    
    #create lists containing unique keys, row and column
    unique_item = sorted(list(set(data[item])))
    
    return unique_item    

#sort the rows of pivot table by the number of empty elements in each row
def sort_pvt_vals(pvt_vals):
    return sorted(pvt_vals, key=lambda x:len(([num for num in x[1] if num < 0])))

#create a table of aggregation values
def get_pvt_vals(data, row, col, val, mode, unique_row, unique_col):

    #create a list containing values of aggregation corresponding to unique_row and unique_col
    pvt_vals = [] 
    #used for sorting
    count = 0

    for row_item in unique_row:

        temp_row = []

        if row in ['Season','Tm']:
            row_data = get_specific_data(data,row,row_item)
        else:
            row_data = filter_dic(all_data,filter_data_bin(all_data,row,row_item))

        

        for col_item in unique_col:
            
            #get a list of values corresponding to row and column
            if col in ['Season','Tm']:
                needed_data = get_specific_data(row_data,col,col_item)
            else:
                needed_data = filter_dic(row_data,filter_data_bin(row_data,col,col_item))
            

            if(needed_data):
                
                
                #sum mode
                if mode == "SUM":

                    tot = sum(map(int,needed_data[val]))
                    temp_row.append(tot)
                
                elif mode == "COUNT":
                    count = len(needed_data[val])
                    temp_row.append(tot)    
                
                else:
                    
                    average = int(tot / float(len(needed_data[val])))
                    temp_row.append(average)

            #for blank cell 
            else:

                temp_row.append(-1)
            
        pvt_vals.append((count, temp_row))
        count += 1
            
    return sort_pvt_vals(pvt_vals)

#returns string of html coding a pivot table
def create_table_str(pvt_vals, unique_row):
    
    table_str = '<tbody>\n'

    for index in range(len(pvt_vals)):

        table_str += '<tr>\n<td>%d</td>\n<td>%s</td>\n'%(pvt_vals[index][0], unique_row[pvt_vals[index][0]])

        for item in pvt_vals[index][1]:

            if(item >= 0):            
                table_str += '<td>%d</td>\n'%(item)
            else:
                table_str += '<td></td>\n'

    table_str += '</tbody>\n'
  
    return table_str





def create_filter_dic(atts):
    filter_dic = {}
    for item in atts:
        filter_dic[item] = [] 

    return filter_dic

def filter_dic(data,index):

    filter_dic = create_filter_dic(data.keys())

    for key in data.keys():

        for i in range(len(data[key])):

            if i in index:
                filter_dic[key].append(data[key][i])

    return filter_dic


def filter_data_bin(data,filter_by,filter_val):

    store = []

    for index in range(len(data[filter_by])):

        if filter_by in ['WS','eFG%','Age']:

            val = float(data[filter_by][index])
  
        else:
            val = float(data[filter_by][index])/SEASON_LENGTH

        if val >= filter_val[0] and val < filter_val[1]:
                        store.append(index)

    return store



def filter_row_col(row_index,col_index):
    return list(set.intersection(set(row_index),set(col_index)))


def att_intervals():

    interval = {}
    interval['AST'] = ASSISTS_INTERVAL
    interval['Age'] = AGE_INTERVAL
    inteval['WS'] = WS_INTERVAL
    interval['PTS'] = PTS_INTERVAL
    interval['eFG%'] = EFG_INTERVAL
    interval['STL'] = STL_INTERVAL
    interval['BLK'] = BLK_INTERVAL
    interval['STL'] = STL_INTERVAL
    interval['TOV'] = TOV_INTERVAL

    return interval

def min_max(data,item):
    converted = map(float,data[item])
    return  (min(converted),max(converted))



def get_bin_header(start,end,interval):

    curr = start
    header = []

    while curr < end:
        header.append((curr,curr+interval))
        curr = curr+interval

    return header

def get_bin_str(header):

    bin_str = []

    for i in range(len(header)):

        bin_str.append(str(header[i][0]) + "to" +str(header[i][1]))

    return bin_str






all_data = get_all_data('dataclean.csv')

kobe = get_index(all_data,'Player','Kobe Bryant')

header = get_bin_header(0,MAX_AST_PG,1)
header_str = get_bin_str(header)
print header_str

        
