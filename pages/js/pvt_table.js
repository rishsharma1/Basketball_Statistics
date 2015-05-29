$(document).ready(function() {

    //load pivot table for the first time
    this.count = ++this.count || 1
    if (typeof this.count != 1) {
        var rows = $("#pTable"); 
        var new_rows = rows.find("tr")
        rows.find("tr").remove();
        rows.append(new_rows);
    }

    //transpose pivot table
    $("#trans_btn").click(function() {
        
        this.count = ++this.count || 1
        if (this.count % 2 != 0) {
            $('link[href="pages/css/pvt_style.css"]').attr('href','pages/css/pvt_style_trans.css');
        } else {
            $('link[href="pages/css/pvt_style_trans.css"]').attr('href','pages/css/pvt_style.css');              
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
            $("#pTable").trigger(esc);
    });

    //redirect to contoroller.py
    $("#select_btn").click(function() {
        window.location.href="controller.py";
    });

    //switch total and mean 
    $("#switch_btn").click(function() {
        this.count = ++this.count || 1
        var flag = this.count % 2 != 0;
        var row_sum = [];
        var col_sum = [];
        
        if (flag === true) {
            ($("#pTable").find("tr").first()).find("th").last().html("Mean ");
            ($("#pTable").find("tr").last()).find("th").first().html("Mean ");
        } else {
            ($("#pTable").find("tr").first()).find("th").last().html("Total");
            ($("#pTable").find("tr").last()).find("th").first().html("Total");
        }
 
        var row_count = 0;        
        $("#pTable").find("tr").not(':first').not(':last').each(function(){
            
            var col_sum_tmp = 0;
            var col_sum_cnt = 0;
            var col_count = 0;
          
            $(this).find("td").not(':last').each(function(){
                var check_num = $(this).html();
                if ($.isNumeric(check_num)) {
                    var temp = Number(check_num);
                    col_sum_tmp += temp;
                    col_sum_cnt += 1;
                    
                    if (row_sum[col_count] === undefined ) {
                        row_sum[col_count] = [];
                        row_sum[col_count][0] = temp;
                        row_sum[col_count][1] = 1;
                    } else {
                        row_sum[col_count][0] += temp;
                        row_sum[col_count][1] += 1;
                    }
                }
                col_count += 1;
            });
            col_sum[row_count] = [];
            col_sum[row_count][0] = col_sum_tmp;
            col_sum[row_count][1] = col_sum_cnt;
            row_count += 1;
        });

        var row_count = 0;
        $("#pTable").find("tr").not(':first').not(':last').each(function(){
            var temp = col_sum[row_count];
            //mean
            if (flag === true) {
                $(this).find("td").last().html((temp[0]/temp[1]).toFixed(2));
            //sum
            } else {
                if (Math.floor(temp[0]) == temp[0]) {
                    $(this).find("td").last().html(temp[0].toFixed(0));
                } else {                
                    $(this).find("td").last().html(temp[0].toFixed(2));
                }
            }
            row_count += 1;
        });   
        
        var col_count = 0;
        $("#pTable").find("tr").last().each(function(){
            $(this).find("td").not(':last').each(function(){
                var temp = row_sum[col_count]
                if (flag === true) {
                    $(this).html((temp[0]/temp[1]).toFixed(2));
                } else {
                    if (Math.floor(temp[0]) == temp[0]) {
                        $(this).html(temp[0].toFixed(0));
                    } else {
                        $(this).html(temp[0].toFixed(2));
                    }
                }
                col_count += 1;
            });  
        });             
    });
});

