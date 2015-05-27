import math
import data

HEADER_COLOUR = 'hsla(360,0%,50%,0.2)'    #pivot table header colour
BLANK_COLOUR = 'hsla(360,0%,95%,0.4)'     #colour for blank cells
FOOTER_COLOUR = HEADER_COLOUR    #colour for the total row
BLUE = 235            #the first argument of hsla() representing blue colour
RED = 0               #the first argument of hsla() representing red colour
TH = 'th'             #string representing th table element
TD = 'td'             #string representing td table element
SATURATION = 100      #the number of saturation used for hsla function
OPAQUE = 0.75         #the number of opaqueness used for hsla function
BLUE_BOUNDARY = 50    #relative percentage of pivot table value below which blue colour is assigned
RED_BOUNDARY = 51     #relative percentage of pivot table value above which blue colour is assigned
MAX_LIGNTNESS = 98    #maximum number of lightness argument of hsla function
ROW_HEADER_LEN = 1    #the length the row header occupies rows of the pivot table
COL_HEADER_LEN = 1    #the length the column header occupies columns of the pivot table

PIVOT_CSS = 'pages/css/pvt_style.css'

KEYWORD_DICT = {
"Season":"Season",
"Tm":"Team",
"AST":"Assists (Bin)",
"PTS":"Points (Bin)",
"Age":"Age (Bin)",
"eFG%":"eFG&#37; (Bin)",
"WS":"Win Share (Bin)",
"BLK":"Blocks (Bin)",
"STL":"Steals (Bin)",
"TOV":"Turnovers (Bin)",
"AVE":"Average of",
"SUM":"Sum of",
"COUNT":"Count of",
"MAX":"Max of",
"MIN":"Min of"
}


def create_header():
    
    header_str =  'Content-Type: text/html\n\n'
    header_str += '<!DOCTYPE html>\n'
    header_str += '<html>\n'
    header_str += '<head>\n'
    header_str += '    <title>Select Data</title>\n'
    header_str += '    <!-- this ensures mobile phones don\'t display desktop versions -->\n'
    header_str += '    <meta name="viewport" content="width=device-width,intial-scale=1.0">\n'
    header_str += '    <link href="pages/css/bootstrap.min.css" rel="stylesheet">\n'
    header_str += '    <link href="pages/css/styles.css" rel="stylesheet">\n'
    header_str += '    <!-- import jQuery -->\n'
    header_str += '    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>\n'
    header_str += '    <script src="pages/js/bootstrap.js"></script>\n'
    
    return header_str




def create_nav_bar():
    
    bar_str =  '<body>\n'
    bar_str += '<div class="navbar navbar-inverse navbar-static-top">\n'
    bar_str += '<div class="container">\n'
    bar_str += '    <a href="#"class="navbar-brand">Basketball</a>\n'
    bar_str += '    <button class ="navbar-toggle" data-toggle ="collapse" data-target =".navHeaderCollapse">\n'
    bar_str += '        <span class = "icon-bar"></span>\n'
    bar_str += '        <span class = "icon-bar"></span>\n'
    bar_str += '        <span class = "icon-bar"></span>\n'
    bar_str += '    </button>\n'
    bar_str += '    <div class="collapse navbar-collapse navHeaderCollapse">\n'
    bar_str += '        <ul class="nav navbar-nav navbar-left">\n'
    bar_str += '            <li><a href="#">Home</a></li>\n'
    bar_str += '            <li><a href="pages/select.html">Select Data</a></li>\n'
    bar_str += '             <li><a href="pages/analysis.html">Analysis</a></li>\n'
    bar_str += '        </ul>\n'
    bar_str += '    </div>\n'
    bar_str += '</div>\n'
    bar_str += '</div>\n'
    
    return bar_str

def css_header():
    
    table_css_str =  '<style>\n'
    table_css_str += '    html, body, table {\n'
    table_css_str += '    width: 100%;\n'
    table_css_str += '    height: 100%;\n'
    table_css_str += '    margin: 0;\n'
    table_css_str += '}\n'
    table_css_str += '#t_header {\n'
    table_css_str += '    margin-bottom:30px;\n'
    table_css_str += '}\n'
    table_css_str += '#pTable td, #pTable th {\n'
    table_css_str += '    margin: 0;\n'    
    table_css_str += '    text-align: center;\n'
    table_css_str += '    vertical-align: center;\n'
    table_css_str += '    border: 0 !important;\n'
    table_css_str += '}\n'
    
    return table_css_str


#create header of pivot table
def create_table_header(row, unique_col):
    
    theader_str = '<tr>\n<th></th>\n'
    
    for col in unique_col:
        theader_str += '<th>%s</th>\n'%(col)
    
    theader_str += '</tr>\n'
    return theader_str




# takes a sorted list to create a list containing lower and upper threshold values
# any data outside the thresholds are regarded as outliers
def get_outlier_thresholds(sList):
    
    q1 = 0.0    #lower quartile
    q3 = 0.0    #upper quartile
    median = 0.0
    mRank = ((len(sList) + 1) / 2.0)       # The median rank

    # calculate median.
    if mRank % 2.0 != 0:
        median = (sList[int(math.floor(mRank)) - 1] + sList[int(math.ceil(mRank)) - 1]) / 2.0
    else:
        median = sList[int(mRank) - 1]
    
    # calculate lower and upper quartiles
    lRank = (math.floor(mRank) + 1) / 2.0        # The lower quartile rank
    uRank = len(sList) - lRank + 1        # The upper quartile rank
    
    if lRank % 2.0 != 0:
        q1 = (sList[int(math.floor(lRank)) - 1] + sList[int(math.ceil(lRank)) - 1]) / 2.0
        q3 = (sList[int(math.floor(uRank)) - 1] + sList[int(math.ceil(uRank)) - 1]) / 2.0
    else:
        q1 = sList[int(lRank) - 1]
        q3 = sList[int(uRank) - 1]
        
    #calculate interquartile difference
    iqd = q3 - q1
    lThsld = q1 - 1.5 * iqd if q1 - 1.5 * iqd >= 0 else 0
    uThsld = q3 + 1.5 * iqd
    
    
    return [lThsld, uThsld]





#returns a string of nth-child css element 
def get_nth_child(elm, row, col, colour):
    
    nth_child_str =  '#pTable tr:nth-child(%d) %s:nth-child(%d) {\n'%(row, elm, col)
    nth_child_str += '    background: %s;\n'%(colour)
    nth_child_str += '}\n' 
    
    return nth_child_str




#create css of pivot table
def create_table_css(pvt_vals, row_len, col_len):

    table_css_str = css_header()
    
    #max and min of sum or average corresponding to unique_row and unique_col
    minval, maxval = get_outlier_thresholds(sorted(
    [val for i in range(len(pvt_vals)) for val in pvt_vals[i][1] if val >= 0 and type(val) != str]))
    
    
    #apply colours to the table headings
    for row_cnt in range(1, row_len+ROW_HEADER_LEN+1):
        
        for col_cnt in range(1, col_len+COL_HEADER_LEN+2):

            #first row
            if row_cnt == 1:
                
                table_css_str += get_nth_child(TH, row_cnt, col_cnt, HEADER_COLOUR)
                
            #the first column of the bottom row (total row)
            elif col_cnt == 1 and row_cnt == row_len+ROW_HEADER_LEN:

                table_css_str += get_nth_child(TH, row_cnt, col_cnt, FOOTER_COLOUR)
                
            #first column   
            elif col_cnt == 1:
                
                table_css_str += get_nth_child(TH, row_cnt, col_cnt, HEADER_COLOUR)
                                          
            continue
                
    #apply colours to table contents
    for row_cnt in range(ROW_HEADER_LEN+1, row_len+ROW_HEADER_LEN+1):
        for col_cnt in range(COL_HEADER_LEN+1, col_len+COL_HEADER_LEN+1):  
            
            #get the value of each table cell
            pvt_val = pvt_vals[row_cnt-ROW_HEADER_LEN-1][1][col_cnt-COL_HEADER_LEN-1]
            
            #if table cell is not blank, calculate colour
            if(pvt_val > 0 and pvt_val != 'null'):               

                # adjust outliers to the threshold values
                if pvt_val < minval:
                    pvt_val = minval
                if pvt_val > maxval:
                    pvt_val = maxval

                #the bottom row (total row)
                if row_cnt == row_len+ROW_HEADER_LEN:
                    colour = FOOTER_COLOUR     
                #if there is only one value, apply "blank colour" to the entire table
                elif maxval == minval:
                    colour = BLANK_COLOUR
                else :
                    rel_pos = int(abs(math.ceil((((pvt_val - minval) / float(maxval - minval)) * 100))))

                    #calculation of colour according to the relative position of each table value
                    if rel_pos >= RED_BOUNDARY:
                        colour = 'hsla(%d,%d%%,%d%%,%f)'%(RED, SATURATION, 
                        MAX_LIGNTNESS-int((rel_pos-RED_BOUNDARY)*((MAX_LIGNTNESS-BLUE_BOUNDARY)/float(MAX_LIGNTNESS/2))), OPAQUE)     
                    else:
                        colour = 'hsla(%d,%d%%,%d%%,%f)'\
                            %(BLUE, SATURATION, BLUE_BOUNDARY+int(rel_pos*((MAX_LIGNTNESS-BLUE_BOUNDARY)/float(BLUE_BOUNDARY))), OPAQUE) 

                table_css_str += get_nth_child(TD, row_cnt, col_cnt, colour)
                
            #if table cell is blank, apply "blank colour" to the cell    
            else:
                
                #the bottom row (total row)
                if row_cnt == row_len+ROW_HEADER_LEN:
                    colour = FOOTER_COLOUR   
                else:
                    colour = BLANK_COLOUR 
                    
                table_css_str += get_nth_child(TD, row_cnt, col_cnt, colour)                  

    table_css_str += '</style>\n' 
    
    #write css file for table
    css_file = open(PIVOT_CSS,'w')
    css_file.write(table_css_str)
    css_file.close()

    return '<link rel="stylesheet" type="text/css" href="%s">\n'%(PIVOT_CSS)





#returns string of html coding a pivot table
def create_table_str(pvt_vals, unique_row):
    
    table_str = '<tbody>\n'

    for index in range(len(pvt_vals)):

        table_str += '<tr>\n'
        table_str += '<th>%s</th>\n'%( unique_row[pvt_vals[index][0]])

        for item in pvt_vals[index][1]:

            #put empty cell
            if item == 'null' :
                table_str += '<td></td>\n'
            #check for int formatting 
            elif item.__class__.__name__ == 'int':              
                table_str += '<td>%d</td>\n'%(item)
            #check for float for formatting 
            else:
                table_str += '<td>%s</td>\n'%("{0:.2f}".format(item))                                                 

        table_str += '</tr>\n' 

    table_str += '</tbody>\n'

    return table_str




#this function takes the table_str,and row and col headers
#to create the html for the table with the css 
def print_table(pvt_vals,title_str, row, unique_row, unique_col, table_str):
    
    output = create_header()
    
    output += create_table_css(pvt_vals, len(unique_row), len(unique_col))
    
    output += '</head>\n'    
    output += create_nav_bar()

    #add styling here
    output += '<div class="container">\n'
    output +=  title_str
    output += '<div class="table-responsive">\n'
    output += '<table id="pTable" class="table table-borderless table-hover">\n'
    output += create_table_header(row, unique_col)
    output += table_str
    output += '</table>\n</div>\n</div>\n</body>\n</html>\n'
    
    print output
    
    
    

#prints html code of error page
def print_error(err_msg):
    output =  create_header()
    output += '</head>\n'    
    output += create_nav_bar()
    output += '<div class="container">\n'
    output += '<div><h2>Error</h2></div>\n'
    output += '<body>\n'
    output += '<h2>%s</h2>\n'%(err_msg)
    output += '</body>\n'
    output += '</html>\n'

    print output
    
    
    

#prints html page that will redirect to select.html
def print_select():

    select_str =  'Content-Type: text/html\n\n'
    select_str += '<!DOCTYPE html>\n'
    select_str +=  '<html>\n'
    select_str += '<head>\n'
    select_str += '<meta http-equiv="refresh" content="0; url=pages/select.html"/>\n'
    select_str += '</head>\n'
    select_str += '</html>\n'

    print select_str
    


def translate(keyword):
    if keyword in KEYWORD_DICT.keys():
        return KEYWORD_DICT[keyword]
    else:
        return keyword
    
    


def create_title(row, col, val, mode, searchby, search):
    row = translate(row)
    col = translate(col)
    val = translate(val)
    val = val.replace(' (Bin)','')
    mode = translate(mode)
    
    if (searchby == row) and search:
        row += ' (%s)'%(search)
    elif search:
        col += ' (%s)'%(search)
    
    
    title_str = '<div class="page-header"><h2>{} {} By {} and {}</h2></div>\n'.format(mode, val, row, col)

    return title_str




    
