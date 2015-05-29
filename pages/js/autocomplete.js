$(function() {
    
    $( "#searchbox" ).focus(function() {
       
        var mode = $( "#searchby option:selected" ).val();
        var availableTags;
    
        if ( mode == "Season") {
  
            availableTags = [ "1999-00", "2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06", "2006-07" ];

        
        } else if (mode == "Tm" ) {
        
            availableTags = [ "ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", 
                              "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", 
                              "SAS", "TOR", "UTA", "WAS", "NJN", "SEA", "CHH", "NOK", "NOH", "VAN" ];
    
        }

        $( "#searchbox" ).autocomplete({
              source: availableTags
        });        
    });
});      

