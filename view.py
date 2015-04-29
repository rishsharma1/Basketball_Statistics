

def create_header():

    return """Content-Type: text/html\n\n
              <!DOCTYPE html>
              <html>
    
              <head>
                  <title>Select Data</title>
        
        
                <!-- this ensures mobile phones don't display desktop versions -->
                <meta name="viewport" content="width=device-width,intial-scale=1.0">
                <link href="pages/css/bootstrap.min.css" rel="stylesheet">
                <link href="pages/css/styles.css" rel="stylesheet">
        
                </head>"""


def create_nav_bar():
    return """<body>

                   <!-- import jQuery -->
                  <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
                     <script src="js/bootstrap.js"></script>
        
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
                                <li><a href="pages/select.html">Select Data</a></li>
                                 <li><a heref="#">About</a></li>
                            </ul>
                        </div>
                  
                    </div>
                    
                </div>"""

def create_table(table_str):
    output = create_header()+create_nav_bar()

    #add styling here
    output += """<table class="table table-striped table-bordered table-hover" style="width: auto;" align ="center">"""
    print output+table_str