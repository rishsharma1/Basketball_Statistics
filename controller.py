import cgi
import data
import view
import os

#check the file from which this controller was called
prev_addr = os.getenv('HTTP_REFERER')
prev_page = None 
if prev_addr != None:
    prev_page = prev_addr.split('/')[-1]

if prev_page == 'select.html':

    form = cgi.FieldStorage()
    
    #get values sent via form
    row = form.getvalue("row")
    col = form.getvalue("col")
    val = form.getvalue("val")
    mode = form.getvalue("mode")
    searchby = form.getvalue("searchby")
    search = form.getvalue("search")
    
    try:
        
        all_data = data.get_all_data('dataclean.csv')
        interval = data.att_intervals()
        
        

        #get key elements from row and column 
        if row in ['Season','Tm']:
            unique_row = data.create_keys(all_data, row)
            unique_row_str = unique_row
        else:
            row_min_max = data.min_max(all_data,row)
            unique_row = data.get_bin_header(row_min_max[0],row_min_max[1],interval[row])
            unique_row_str = data.get_bin_str(unique_row)

        if col in ['Season','Tm']:
            unique_col = data.create_keys(all_data,col)
            unique_col_str = unique_col
        else:
            col_min_max = data.min_max(all_data,col)
            unique_col = data.get_bin_header(col_min_max[0],col_min_max[1],interval[col])
            unique_col_str = data.get_bin_str(unique_col)
        #if search query is passed, filter unique_row or unique_col using the query
        if searchby and search:
        
            if row == searchby:
                temp = [item for item in unique_row if item == search]
                if temp != []:
                    unique_row = temp
                else:
                    raise ValueError('No item was found')
        
            elif col == searchby:
                temp = [item for item in unique_col if item == search]
                if temp != []:
                    unique_col = temp
                else:
                    raise ValueError('No item was found')
    
        
        #get pivot table values
        pvt_vals = data.get_pvt_vals(all_data, row, col, val, mode, unique_row, unique_col)
       
        
        
        #get html of the pivot table contents

        html_str = data.create_table_str(pvt_vals, unique_row_str)
        #print html_str
        
        if(html_str):
            view.print_table(pvt_vals, row, unique_row_str, unique_col_str, html_str)
    
    except ValueError as val_err:

        view.print_error(val_err)

else:

    view.print_select()

