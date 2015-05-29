import csv
from collections import defaultdict

#----------CONSTANTS--------------#

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
DATA_FILE = 'dataclean.csv'

#---------------------------------#


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



#returns unique row or column keys 
def create_keys(data, item):
    
    #create lists containing unique keys, row and column
    unique_item = sorted(list(set(data[item])))
    
    return unique_item



#sort the rows of pivot table by the number of empty elements in each row
def sort_pvt_vals(pvt_vals):
    return sorted(pvt_vals, key=lambda x:len(([num for num in x[1] if num < 0])))




#return the summation of the data
#only vals that are valid 
def sum_data(data):
    
    tot = sum([val_type(item)(item) for item in data if val_type(item) != str])
    return tot




#return the count of the data 
def count_data(data,row,col,val):
    
    #special cases 
    if val in ['Season','Tm']:
        count_items = len(list(set(data)))
    else:    
        count_items = len(data)
    
    return count_items




#return the average of the data
#depending on what the row,col and val are, so average is
#calculated correctly across all the attributes 
def average_data(data,row,col,val):
    
    
    if val in ['WS','eFG%','Age']:
                        
        tot = sum([val_type(item)(item) for item in data[val] if val_type(item) != str])
        average = tot/ float(len(data[val]))
                        
                    
    else:
                        
        if row in ['Season','Tm'] and col in ['Season','Tm']:
            average = sum(map(val_type(data[val][0]),
            data[val]))/float(SEASON_LENGTH)
        else:
            average = sum(map(val_type(data[val][0]),
            data[val]))/float(sum(map(val_type(data['G'][0]),data['G'])))
    
    return average


            

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
            row_data = filter_dic(data,filter_data_bin(data,row,row_item))

        

        for col_item in unique_col:
            
            #get a list of values corresponding to row and column
            if col in ['Season','Tm']:
                
                needed_data = get_specific_data(row_data,col,col_item)
            else:
                
                needed_data = filter_dic(row_data,filter_data_bin(row_data,col,col_item))     

            if(needed_data and len(needed_data[val])>0):
                
                #sum mode
                if mode == "SUM":
                    
                    temp_row.append(sum_data(needed_data[val]))
                
                #count mode
                elif mode == "COUNT":
                        
                    temp_row.append(count_data(needed_data[val],row,col,val))    
                
                #average mode 
                else:
                         
                    temp_row.append(average_data(needed_data,row,col,val))
                    

            #for blank cell 
            else:
                #using 'null' to reperesent empty vals
                temp_row.append('null')

        pvt_vals.append((count, temp_row))
        count += 1
        
    return sort_pvt_vals(pvt_vals)





#for each row and column of pivot table, we
#want to sum the list of values, as long as they
#are not null,and then append the total of each row
# and each column back into the pvt_table 
def pvt_table_total(pvt_table):
    
    #making space for the totals in pvt_table    
    pvt_table.append((pvt_table[-1][0]+1,[]))  
    
    #calculate sum of rows of each column   
    for index in range(len(pvt_table[0][1])):
        
        sum = 0
        for row in range(len(pvt_table)-1):
            
            #don't want a null
            if type(pvt_table[row][1][index]) != str:
                sum += pvt_table[row][1][index]

        pvt_table[-1][1].append(sum)                                                      
    
    #calculate sum of columns of each row
    for row in range(len(pvt_table)):
        sum = 0
        for col in range(len(pvt_table[row][1])):
            col_val = pvt_table[row][1][col]
            if type(col_val) != str:
                sum += col_val
                
        if row != len(pvt_table)-1:
            pvt_table[row][1].append(sum)
        else:
            pvt_table[row][1].append('null')    
        
    return pvt_table

    
        
        
#filter dic creates a dictionary with all the attributes
#that we are using from the csv file, making it easier for
#us to filter data out.Check readme for attributes names.
def create_filter_dic(atts):
    
    filter_dic = {}
    for item in atts:
        filter_dic[item] = [] 

    return filter_dic




#filter dic takes in some data, and a list of
#indicies, which are the position of vals that
#are to be used.The function returns the filtered
#dictionary with the specified vals 
def filter_dic(data,index):
    
    #create an empty dictionary with relevant attributes
    filter_dic = create_filter_dic(data.keys())

    for key in data.keys():

        for i in range(len(data[key])):
            
            #only put the vals if they are in index
            if i in index:
                
                filter_dic[key].append(data[key][i])

    return filter_dic




#filter data by bin, takes some data,a filter by
#which is the attributes in the csv file, and filter val
#which is a tuple of a two vals, which is the current 
#interval range of the bin
def filter_data_bin(data,filter_by,filter_val):

    store = []
    

    for index in range(len(data[filter_by])):

        try:
            
            #special cases 
            if filter_by in ['WS','eFG%','Age']:
                
                if val_type(data[filter_by][index]) != str:
                
                    val = val_type(data[filter_by][index])(data[filter_by][index])
                    
            else:
                                   
                val = float(data[filter_by][index])/int(data['G'][index])
                
        except:
            
            continue
        
        #see if any vals are in this range 
        if val >= filter_val[0] and val < filter_val[1]:
                        store.append(index)

    return store




#setting the appropriate interval
#size for each attribute 
def att_intervals():

    interval = {}
    interval['AST'] = ASSISTS_INTERVAL
    interval['Age'] = AGE_INTERVAL
    interval['WS'] = WS_INTERVAL
    interval['PTS'] = PTS_INTERVAL
    interval['eFG%'] = EFG_INTERVAL
    interval['STL'] = STL_INTERVAL
    interval['BLK'] = BLK_INTERVAL
    interval['STL'] = STL_INTERVAL
    interval['TOV'] = TOV_INTERVAL

    return interval



#for some item, which is the attributes in the csv
#file we want to find the minimum and maximum value
def min_max(data,item):

    converted = [val_type(val)(val) for val in data[item] if val_type(val) != str ]
    
    
    if item in ['WS','eFG%','Age']:
        return  (min(converted),max(converted))
    
    #rest of the stats are based on per game, So we divide by SEASON_LENGTH
    else:
        return (min(converted)/float(SEASON_LENGTH),max(converted)/float(SEASON_LENGTH))
    
    
    
    
#this returns a list of tuples, consisting of
#intervals from start to end for the binning     
def get_bin_header(start,end,interval):

    curr = start
    header = []

    while curr < end:
        header.append((curr,curr+interval))
        curr = curr+interval

    return header



#for a given bin header see get_bin_header,
#this will ouput a list of tuples with the bin
#header for the pivot table, used in the html
def get_bin_str(header):

    bin_str = []

    for i in range(len(header)):

        bin_str.append(str(header[i][0]) + "-" +str(header[i][1]))

    return bin_str



#used for determining the 
#if a float is in string, or an integer 
def val_type(val):
    
    for i in [int,float]:
        try:
            i(val)
            return i
        except ValueError:
            continue
    return str  





        
