import math

#coloring codes
table_color = ['#CC7A00','#E68A00','#FF9900','#FFA319','#FFAD33','#FFB84D',
                '#FFC266','#FFCC80','#FFD699','#FFE0B2','#FFEBCC','#FFF5E6',
                '#EBEBFF','#D6D6FF','#C2C2FF','#ADADFF','#9999FF','#8585FF',
                '#7070FF','#5C5CFF','#4747FF','#3333FF','#2E2EE6','#2929CC'] 
table_color = table_color[::-1]

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
    bar_str += '             <li><a heref="#">About</a></li>\n'
    bar_str += '        </ul>\n'
    bar_str += '    </div>\n'
    bar_str += '</div>\n'
    bar_str += '</div>\n'
    
    return bar_str

#create header of pivot table
def create_table_header(row, unique_col):
    
    theader_str = '<thead>\n<tr>\n<th>%s</th>\n<th>%s</th>\n'%('index', row)
    
    for col in unique_col:
        theader_str += '<th>%s</th>\n'%(col)
    
    theader_str += '</tr>\n</thead>\n'
    return theader_str

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
    table_css_str += '    text-align: center;\n'
    table_css_str += '    vertical-align: center;\n'
    table_css_str += '}\n'

    #max and min of sum or average corresponding to unique_row and unique_col
    maxval = max([max(pvt_vals[i][1]) for i in range(len(pvt_vals))])
    minval = min([min([val for val in pvt_vals[i][1] if val >= 0]) for i in range(len(pvt_vals))])
    agg_count = 0

    #give colours to each cell of the table
    for row_cnt in range(0, row_len+1):
        for col_cnt in range(1, col_len+1+2):

            if row_cnt == 0:
                table_css_str += 'tr:nth-child(%d) th:nth-child(%d) {\n'%(row_cnt+1, col_cnt)
                table_css_str += '    background: %s;\n'%('#F9F9F9')
                table_css_str += '}\n'                 
                continue
            elif col_cnt == 1 or col_cnt == 2:
                table_css_str += 'tr:nth-child(%d) td:nth-child(%d) {\n'%(row_cnt, col_cnt)
                table_css_str += '    background: %s;\n'%('#FFFFFF')
                table_css_str += '}\n'                 
                continue
            
            if(pvt_vals[row_cnt-1][1][col_cnt-3] > 0):            

                if True:    

                    #pick a color by calculating the relative position of the cell value using hsl
                    rel_pos = int(abs(math.ceil((((pvt_vals[row_cnt-1][1][col_cnt-3] - minval) / float(maxval - minval)) * 100))))
                    table_css_str += '/* rel_pos=%d */\n'%(rel_pos)
                    if rel_pos >= 51:
                        colour = 'hsla(%d,%d%%,%d%%,%f)'%(235, 100, 98-int((rel_pos-51)*(45/float(49))), 0.8)    
                    
                    else:
                        colour = 'hsla(%d,%d%%,%d%%,%f)'%(0, 100, 50+int(rel_pos*(48/float(50))), 0.8)    
    
                if False:    

                    #pick a color by calculating the relative position of the cell value by hardcoding 
                    colour = table_color[int(abs(math.ceil((((pvt_vals[row_cnt-1][1][col_cnt-3] - minval) / float(maxval - minval)) * 24) - 1)))]
                    
                table_css_str += 'tr:nth-child(%d) td:nth-child(%d) {\n'%(row_cnt, col_cnt)
                table_css_str += '    background: %s;\n'%(colour)
                table_css_str += '}\n'                 

            else:
                
                table_css_str += 'tr:nth-child(%d) td:nth-child(%d) {\n'%(row_cnt, col_cnt)
                table_css_str += '    background: %s;\n'%('#FFFFFF')
                table_css_str += '}\n'                 

            agg_count += 1

    table_css_str += '</style>\n' 
    
    css_file = open('pvt_style.css','w')
    css_file.write(table_css_str)
    css_file.close()

    return '<link rel="stylesheet" type="text/css" href="pvt_style.css">\n'

def print_table(pvt_vals, row, unique_row, unique_col, table_str):
    output = create_header()
    output += create_table_css(pvt_vals, len(unique_row), len(unique_col))
    output += '</head>\n'    
    output += create_nav_bar()

    #add styling here
    output += '<div class="container">\n'
    output += '<div class="page-header"><h2>Pivot Table</h2></div>\n'
    output += '<div class="table-responsive">\n'
    output += '<table class="table table-bordered table-hover">\n'
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




    
