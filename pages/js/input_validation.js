function read_error_msg() {
   var err = document.getElementById("error").value;
   if(!err.length) {
      alert(err);
      return false;
   }
}

<!-- input value check -->
function check_form_vals() {
    var count = ['Season','Player'];
    var average_exc = ['Season','Tm','Player'];
    var sum_exc = average_exc;
    var row = document.forms["pvt_form"]["row"].value;
    var col = document.forms["pvt_form"]["col"].value;
    var mode = document.forms["pvt_form"]["mode"].value;
    var val = document.forms["pvt_form"]["val"].value;
    var searchby = document.forms["pvt_form"]["searchby"].value;
    var search = document.forms["pvt_form"]["search"].value;


    
    if (row == col) {
        document.getElementById("errorbox").style.display = 'block';
        document.getElementById("errormsg").innerHTML = "Row and Column must have different values.";   
        return false;
    
    } else if ((search != "") && (row != searchby && col != searchby)) {
        document.getElementById("errorbox").style.display = 'block';
        document.getElementById("errormsg").innerHTML = "Search category must be row or column.";  
        return false;
    } else if  (mode == 'AVE') {
        
        if(average_exc.indexOf(val) >= 0) {
                
            document.getElementById("errorbox").style.display = 'block';
            document.getElementById("errormsg").innerHTML = "Aggregation not valid.";   
            return false;
        }
        
    } else if (mode == 'SUM') {
        
        if(sum_exc.indexOf(val) >= 0) {
           
            document.getElementById("errorbox").style.display = 'block';
            document.getElementById("errormsg").innerHTML = "Aggregation not valid.";   
            return false;
        }
    } else if (mode == 'COUNT') {
        
        if(!(count.indexOf(val) >= 0)) {
            
            document.getElementById("errorbox").style.display = 'block';
            document.getElementById("errormsg").innerHTML = "Aggregation not valid.";   
            return false;
        }
    }
}


<!-- hide error box -->
function hide_error() {
    document.getElementById("errorbox").style.display = 'none';
}


