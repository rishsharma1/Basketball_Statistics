import cgi
import data
import view



form = cgi.FieldStorage()

#get values sent via form
row = form.getvalue("row")
col = form.getvalue("col")
val = form.getvalue("val")
mode = form.getvalue("mode")
searchby = form.getvalue("searchby")
search = form.getvalue("search")

#get pivot table 
html_str = data.create_table_str(row, col, val,mode,searchby,search)

if(html_str):
    view.create_table(html_str)
