import cgi
import data
import view
import os

PIVOT = 'select.html'
SEARCH_ERROR = 'No item was found'

def main():
        
    
    prev_addr = os.getenv('HTTP_REFERER')
    prev_page = None
    if prev_addr != None:
        prev_page = prev_addr.split('/')[-1]

    if prev_page == PIVOT:
    
        form = cgi.FieldStorage()

        # get values sent via form

        row = form.getvalue('row')
        col = form.getvalue('col')
        val = form.getvalue('val')
        mode = form.getvalue('mode')
        searchby = form.getvalue('searchby')
        search = form.getvalue('search')

        try:

            all_data = data.get_all_data(data.DATA_FILE)
            interval = data.att_intervals()

            # get key elements from row and column

            if row in ['Season', 'Tm']:
                #get unique values for row 
                unique_row = data.create_keys(all_data, row)
                #row header for table str 
                unique_row_str = unique_row
            else:
                #find the min and max value for row
                row_min_max = data.min_max(all_data, row)
                #row header
                unique_row = data.get_bin_header(row_min_max[0],row_min_max[1], interval[row])
                #row header for table str
                unique_row_str = data.get_bin_str(unique_row)

            if col in ['Season', 'Tm']:
                #get unique values for col
                unique_col = data.create_keys(all_data, col)
                #row header for table col
                unique_col_str = unique_col
            else:
                #find the min and max value for col
                col_min_max = data.min_max(all_data, col)
                #col header
                unique_col = data.get_bin_header(col_min_max[0],col_min_max[1], interval[col])
                #col header for table str 
                unique_col_str = data.get_bin_str(unique_col)

            # if search query is passed, filter unique_row or unique_col using the query
            search_row = row
            search_col = col
            if searchby and search:
                
                if row == searchby:
                    temp = [item for item in unique_row if item == search]
                    if temp != []:
                        unique_row = temp
                        unique_row_str = temp
                    else:
                        #item not in csv file
                        raise ValueError(SEARCH_ERROR)
                elif col == searchby:

                    temp = [item for item in unique_col if item == search]

                    if temp != []:
                        unique_col = temp
                        unique_col_str = temp
                    else:
                        raise ValueError(SEARCH_ERROR)

                


            # get pivot table values
            pvt_vals = data.get_pvt_vals(
                all_data,
                row,
                col,
                val,
                mode,
                unique_row,
                unique_col,
                )

            pvt_vals = data.pvt_table_total(pvt_vals, mode)

            # get html of the pivot table contents

            unique_row_str.append('Total')
            title_str = view.create_title(row, col, val, mode, searchby, search)
            html_str = view.create_table_str(pvt_vals, unique_row_str)

            # print html_str
            
            
            if html_str:
                view.print_table(pvt_vals, title_str,row, unique_row_str,unique_col_str, html_str)
        except ValueError, val_err:

            view.print_error(val_err)
    else:

        view.print_select()

main()
        

