$(document).ready(function() {

    this.count = ++this.count || 1
    if (typeof this.count != 1) {
        var rows = $("#pTable"); 
        var new_rows = rows.find("tr")
        rows.find("tr").remove();
        rows.append(new_rows);
    }

    $("#trans_btn").click(function() {
        
        $("#pTable").hide("slow");  
        this.count = ++this.count || 1
        if (this.count % 2 != 0) {
             $('link[href="pvt_style.css"]').attr('href','pvt_style_trans.css');
        } else {
            $('link[href="pvt_style_trans.css"]').attr('href','pvt_style.css');
        }
          var rows = $("#pTable");    
            //temp storage for new rows
            var temp_rows = [];
            //iterate through tr elements
            rows.find("tr").each(function(){
                var col = 1;
                $(this).find("th").each(function(){
                    //the first element in a row is being read
                    if(temp_rows[col] === undefined) { 
                        temp_rows[col] = $("<tr></tr>"); 
                    }
                    temp_rows[col++].append($(this));
                });
                $(this).find("td").each(function(){
                    if(temp_rows[col] === undefined) { 
                        temp_rows[col] = $("<tr></tr>"); 
                    }
                    temp_rows[col++].append($(this));
                });
            });
            //remove all tr elements in the original table
            rows.find("tr").remove();
            //append the transposed rows to the emptied space
            rows.append(temp_rows);
            
            $("#pTable").show("fast");
            
    });

    $("#select_btn").click(function() {
        window.location.href="controller.py";
    });
});

