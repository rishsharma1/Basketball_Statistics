import cgi




print "Content-Type: text/html\n"
form = cgi.FieldStorage()

print """Row: %s, Column: %s,Value: %s,SearchBy: %s,Search: %s"""%(form.getvalue("row"),form.getvalue("col"),form.getvalue("val"),form.getvalue("searchby"),form.getvalue("search"))

