import math
import data

HEADER_COLOUR = '#DADADA'    #pivot table header colour
BLUE = 235
RED = 0
SATURATION = 100    #the number of saturation used for hsla function
OPAQUE = 1.0        #the number of opaqueness used for hsla function
BLUE_BOUNDARY = 50   #relative percentage of pivot table value below which blue colour is assigned
RED_BOUNDARY = 51    #relative percentage of pivot table value above which blue colour is assigned
MAX_LIGNTNESS = 98   #maximum number of lightness argument of hsla function


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
    header_str += '    <script src="js/bootstrap.js"></script>\n'
    
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
    bar_str += '            <li><a heref="#">Home</a></li>\n'
    bar_str += '            <li><a href="pages/select.html">Select Data</a></li>\n'
    bar_str += '             <li><a heref="pages/analysis.html">Analysis</a></li>\n'
    bar_str += '        </ul>\n'
    bar_str += '    </div>\n'
    bar_str += '</div>\n'
    bar_str += '</div>\n'
    
    return bar_str

#create header of pivot table
def create_table_header(row, unique_col):
    
    theader_str = '<thead></th><th></th>'
    
    for col in unique_col:
        theader_str += '<th>%s</th>'%(col)
    
    theader_str += '</tr></thead>'
    return theader_str

# takes a sorted list to create a list containing lower and upper threshold values
# any data outside the thresholds are regarded as outliers
def get_outlier_thresholds(sList):
    
    q1 = 0
    q2 = 0
    median = 0
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
    
    #print "%f %f %f %f"%(q1, q3, lThsld, uThsld)
    return [lThsld, uThsld]

#create css of pivot table
def create_table_css(pvt_vals, row_len, col_len):

    table_css_str =  '<style>\n'
    table_css_str += '    html, body, table {\n'
    table_css_str += '    width: 100%;\n'
    table_css_str += '    height: 100%;\n'
    table_css_str += '    margin: 0;\n'
    table_css_str += '}\n'
    table_css_str += 'table {\n'
    table_css_str += '    border-spacing: 0;\n'
    table_css_str += '}\n'
    table_css_str += 'td, th {\n'
    table_css_str += '    margin: 0;\n'  
    table_css_str += '    text-align: center;\n'
    table_css_str += '    vertical-align: center;\n'
    table_css_str += '}\n'
    table_css_str += '#t_header {\n'
    table_css_str += '    margin-bottom:30px;\n'
    table_css_str += '}\n'
    table_css_str += '.borderless td, .borderless th {\n'
    table_css_str += '    border: none;\n'
    table_css_str += '}\n'
    
    
    #max and min of sum or average corresponding to unique_row and unique_col
    table_css_str += '%s'%(sorted([val for i in range(len(pvt_vals)) for val in pvt_vals[i][1] if val >= 0]))
    minval, maxval = get_outlier_thresholds(sorted([val for i in range(len(pvt_vals)) for val in pvt_vals[i][1] if val >= 0 and type(val) != str]))

    #give colours to each cell of the table
    for row_cnt in range(0, row_len+1):
        for col_cnt in range(2, col_len+1+2):

            if row_cnt == 0 or row_cnt == row_len:
                table_css_str += 'tr:nth-child(%d) th:nth-child(%d) {\n'%(row_cnt+1, col_cnt-1)
                table_css_str += '    background: %s;\n'%(HEADER_COLOUR)
                table_css_str += '}\n'                 
                continue
            elif col_cnt == 2:
                table_css_str += 'tr:nth-child(%d) th:nth-child(%d) {\n'%(row_cnt, col_cnt-1)
                table_css_str += '    background: %s;\n'%(HEADER_COLOUR)
                table_css_str += '}\n'                 
                continue

                 
            
            pvt_val = pvt_vals[row_cnt-1][1][col_cnt-3]
            if(pvt_val > 0 and pvt_val != 'null'):              
                
                # adjust outliers to the threshold values
                if pvt_val < minval:
                    pvt_val = minval
                if pvt_val > maxval:
                    pvt_val = maxval
                    
                #pick a color by calculating the relative position of the cell value using hsl
                
                rel_pos = int(abs(math.ceil((((pvt_val - minval) / float(maxval - minval)) * 100))))
                table_css_str += '/* min=%f, max = %f, rel_pos=%d */\n'%(minval, maxval, rel_pos)

                if rel_pos >= RED_BOUNDARY:
                    colour = 'hsla(%d,%d%%,%d%%,%f)'%(RED, SATURATION, MAX_LIGNTNESS-int((rel_pos-RED_BOUNDARY)*((MAX_LIGNTNESS-                                                      BLUE_BOUNDARY)/float(MAX_LIGNTNESS/2))), OPAQUE)     
                else:
                    colour = 'hsla(%d,%d%%,%d%%,%f)'%(BLUE, SATURATION, 
                    BLUE_BOUNDARY+int(rel_pos*((MAX_LIGNTNESS-BLUE_BOUNDARY)/float(BLUE_BOUNDARY))), OPAQUE) 
                    
                table_css_str += 'tr:nth-child(%d) td:nth-child(%d) {\n'%(row_cnt, col_cnt-1)
                table_css_str += '    background: %s;\n'%(colour)
                table_css_str += '}\n'                 

            else:
                
                table_css_str += 'tr:nth-child(%d) td:nth-child(%d) {\n'%(row_cnt, col_cnt-1)
                table_css_str += '    background: %s;\n'%('#FFFFFF')
                table_css_str += '}\n'                 

    table_css_str += '</style>\n' 
    
    css_file = open('pvt_style.css','w')
    css_file.write(table_css_str)
    css_file.close()

    return '<link rel="stylesheet" type="text/css" href="pvt_style.css">\n'

#returns string of html coding a pivot table
def create_table_str(pvt_vals, unique_row):
    
    table_str = '<tbody>\n'

    for index in range(len(pvt_vals)):

        table_str += '<tr><th>%s</th>'%( unique_row[pvt_vals[index][0]])

        for item in pvt_vals[index][1]:

            if(item >= 0):
                if item == 'null' :
                    table_str += '<td></td>\n'
                elif item.__class__.__name__ == 'int':              
                    table_str += '<td>%d</td>\n'%(item)
                else:
                    table_str += '<td>%s</td>\n'%("{0:.2f}".format(item))                                                 
            else:
                table_str += '<td></td>\n'
                
    

    table_str += '</tbody>\n'

    return table_str

def print_table(pvt_vals, row, unique_row, unique_col, table_str):
    output = create_header()
    
    output += create_table_css(pvt_vals, len(unique_row), len(unique_col))
    output += '</head>\n'    
    output += create_nav_bar()

    #add styling here
    output += '<div class="container">\n'
    output += '<div id="t_header" ><h2>Pivot Table</h2></div>\n'
    output += '<div class="table-responsive">\n'
    output += '<table class="table table-borderless table-hover">\n'
    output += create_table_header(row, unique_col)
    output += table_str
    output += '</table>\n</div>\n</div>\n</body>\n</html>\n'
    
    print output

def print_error(err_msg):
    output =  create_header()
    output += '</head>\n'    
    output += create_nav_bar()
    output += '<div class="container">\n'
    output += '<body>\n'
    output += '<h2>%s</h2>\n'%(err_msg)
    output += '</body>\n'
    output += '</html>\n'

    print output

def print_select():

    select_str =  'Content-Type: text/html\n\n'
    select_str += '<!DOCTYPE html>\n'
    select_str +=  '<html>\n'
    select_str += '<head>\n'
    select_str += '<meta http-equiv="refresh" content="0; url=pages/select.html"/>\n'
    select_str += '</head>\n'
    select_str += '</html>\n'

    print select_str




    
