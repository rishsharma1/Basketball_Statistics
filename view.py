

def create_header():

	return """<!DOCTYPE html>
			  <html>
    
    		  <head>
        	  	<title>Select Data</title>
        
        
        		<!-- this ensures mobile phones don't display desktop versions -->
        		<meta name="viewport" content="width=device-width,intial-scale=1.0">
        		<link href="css/bootstrap.min.css" rel="stylesheet">
        		<link href="css/styles.css" rel="stylesheet">
        
   			 </head>"""
 

def create_nav_bar():
	return """<body>
        
        	  	<div class="navbar navbar-inverse navbar-static-top">
            
           			 <div class="container">
                
                	 	<a href="#"class="navbar-brand">Basketball</a>
                
                		<button class ="navbar-toggle" data-toggle ="collapse" data-target =".navHeaderCollapse">
                    		<span class = "icon-bar"></span>
                    		<span class = "icon-bar"></span>
                    		<span class = "icon-bar"></span>
                		</button>
            
        
                		<div class="collapse navbar-collapse navHeaderCollapse">
                
                    		<ul class="nav navbar-nav navbar-left">
                        		<li><a heref="#">Home</a></li>
                        		<li><a href="select.html">Select Data</a></li>
                         		<li><a heref="#">About</a></li>
                    		</ul>
                		</div>
                  
            		</div>
                    
        		</div>"""