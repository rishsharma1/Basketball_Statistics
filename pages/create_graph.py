import sys
sys.path.insert(0,'../')
import data
#--------------------CONSTANTS------------------------#

SOURCE = "www.basketball-reference.com/"

#first colour represents older seasons,
SEASON_COLOUR = ['rgb(124,181,236)','rgb(67,67,72)']

#min & max steal avg per game and block per game
BLK_STL_MIN_MAX = (1,10)

#high assist avg per game range
HIGH_ASSIST = (5,11)

#low turnover avg per game range
LOW_TURNOVER = (0,2)

#distinguishes old season and new season 
SEASON_CUT_OFF = 4

SEASON_SEPARATOR = '#FF9E28'

ASSIST_FILE = 'assists.js'
PASSING_FILE = 'passing.js'
AVG_TM_FILE = 'avg_tm_points.js'
DEF_COUNT_FILE = 'blk_stl_count.js'
TEAM_DEF_FILE = 'team_def.js'


#-----------------------------------------------------#

#creates a line graph using data, and categories
#determined by header
def create_line(data_vals,header,txt,title,id):
    
    
    
    graph_str  = """$(function () {
        $('#%s').highcharts({
             chart: {
               type: 'line'
             },
    
            title: {
               text: '%s'
            },
            subtitle: {
                text: '%s'
            },
            xAxis: {
    
                plotLines: [{
                    color: '%s',
                    width: 2,
                    value: 3.5
                }],    
                categories: %s
            },
            yAxis: {
                title: {
                    text: '%s'
                }
            },
            plotOptions: {
                
                line: {
    
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
    
            series: [{
                name: 'Season',
                    data: %s
       
                }]
            });
        });"""%(id,title,SOURCE,SEASON_SEPARATOR,header,txt,data_vals)
    
    return graph_str




#creates a pie chart with legends, using
#data vals 
def pie_chart(data_vals,txt,mode,id):

    graph_str = """$(function () {

    $().ready(function () {

        // Build the chart
        $('#%s').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '%s'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [{
                type: 'pie',
                name: '%s',
                data: %s
            }]
        });
    });

    });"""%(id,txt,mode,data_vals)

    return graph_str





#creates a bar graph for data_vals, x-axis is the 
#header 
def create_bar(data_vals,header,text,value,id,min):
    
    graph_str = """$(function () {
    $('#%s').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '%s'
        },
        subtitle: {
            text: '%s'
        },
        xAxis: {
            categories: %s,
            crosshair: true
        },
        yAxis: {
            min: %d,
            title: {
                text: '%s'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} %s</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Old Seasons',
            data:[ """%(id,text,SOURCE,header,min,value,value)
    for i in range(len(data_vals)):
        
        
        graph_str += """{y : %s, color: '%s'}"""%(data_vals[i][0],data_vals[i][1])
        if i != len(data_vals) -1 :
            graph_str += ","
            
    graph_str += """]
                
                }, {name: 'New Seasons',
                    data: []
                }]"""
    graph_str += """});
          });"""
    
     
    
    return graph_str 
    
    
    
def main():
    
        #get all the data     
        all_data = data.get_all_data('../dataclean.csv')
    
        #season header 1999-2007
        header = sorted(list(set(all_data['Season'])))
        
        avg_season_pts = []
        avg_season_def = []
        data_vals = []
        count_tov_ast = []
        count_def = []

        old_season = 0
        new_season = 0
        old_def = 0
        new_def = 0
    
        for (number,season) in enumerate(header):
            
            
            
            #get season data 
            season_data = data.get_specific_data(all_data,'Season',season)
        
            #get points per game of a team from the current season
            season_points = sum(map(int,season_data['PTS']))/float(data.SEASON_LENGTH*len(set(season_data['Tm'])))
            
            #get all assists from current season 
            assists = map(int,season_data['AST'])
            
            #get steals per game of a team from current season  
            season_stl = sum(map(int,season_data['STL']))/float(data.SEASON_LENGTH*len(set(season_data['Tm'])))
            #get blocks per game of a team from current season
            season_blk = sum(map(int,season_data['BLK']))/float(data.SEASON_LENGTH*len(set(season_data['Tm'])))
        
            #the defence accumualtion 
            season_def = season_stl+season_blk
            
            #find the players that have a turnover avg in the range of LOW_TURNOVER
            tov = data.filter_data_bin(season_data,'TOV',LOW_TURNOVER)
        
            #find the players that have a stl avg in the range of BLK_STL_MIN_MAX
            stl = data.filter_data_bin(season_data,'STL',BLK_STL_MIN_MAX)
        
            #find the players that have a blk avg in the range of BLK_STL_MIN_MAX
            blk = data.filter_data_bin(season_data,'BLK',BLK_STL_MIN_MAX)
            
            #find the players that have a assist avg in the range of HIGH_ASSIST
            ast = data.filter_data_bin(season_data,'AST',HIGH_ASSIST)
        
            #find the intersection between low turnover avg players and high assist avg players
            inter_tov_ast = set(tov).intersection(ast)
        
            #find the union of good stealers and good blockers 
            union_def = list(set(blk).union(stl))
            
            #find the average assists of a player for current season 
            avg_ast = sum(assists)/(float(data.SEASON_LENGTH)*len(assists))
            data_vals.append(round(avg_ast,2))
        
            #check if old season or new season 
            if number < SEASON_CUT_OFF:
                
                #add specific colour for old season with the value ready for graphing
                avg_season_pts.append((round(season_points,2), SEASON_COLOUR[0],season))
                avg_season_def.append((round(season_def,2),SEASON_COLOUR[0],season))
                
                #keeping count for old season
                old_season += len(inter_tov_ast)
                old_def += len(union_def)
            
            else:
                
                #add specific colour for new season with the value ready for graphing
                avg_season_pts.append((round(season_points,2), SEASON_COLOUR[1],season))
                avg_season_def.append((round(season_def,2),SEASON_COLOUR[1],season))
                
                #keeping count new season 
                new_season += len(inter_tov_ast)
                new_def += len(union_def)

            

            
        #all data for the pie chart 
        count_tov_ast.append(['Old Seasons',old_season])
        count_tov_ast.append(['New Seasons',new_season])
        count_def.append(['Old Seasons',old_def])
        count_def.append(['New Seasons',new_def])
        
                
        
        #making the graph for Average APG of Player
        assists = open('js/'+ASSIST_FILE,'w')
        assists.write(create_line(data_vals,header,'APG','Average APG of Player from 1999-2007','assists_graph'))
        assists.close()
        
        
        #making the graph for Count of High Performers in Passing 
        passing = open('js/' + PASSING_FILE,'w')
        passing.write(pie_chart(count_tov_ast,
        'Count of High Performers in Passing From 1999-2007','Count','points_graph'))
        passing.close()
        
        
        #sorting the avg_season_pts & avg_season_def by value
        sort_list = sorted(avg_season_pts,reverse=True, key= lambda x:x[0])
        sort_list_def = sorted(avg_season_def,reverse=True,key = lambda x:x[0])
        
        #sorting header accordingly
        new_header = [x[2] for x in sort_list]
        #new_header_def = [x[2] for x in sort_list_def]
        
        
        #making the graph for average team points per game 
        tm_points = open('js/'+ AVG_TM_FILE,'w')
        tm_points.write(create_bar(sort_list,new_header,
        'Average PPG of Teams From 1999-2007','Average PPG','bar_graph',sort_list[-1][0]))
        tm_points.close()
        
        
        #making the graph for Count of High Performers in Defence
        def_count = open('js/'+ DEF_COUNT_FILE,'w')
        def_count.write(pie_chart(count_def,
        'Count of High Performers in Defence From 1999-2007','Count','stl_blk_graph'))
        def_count.close()
        
        #making the graph for average defence per game 
        team_def = open('js/'+ TEAM_DEF_FILE,'w')
        team_def.write(create_bar(avg_season_def,header,
        'Average DPG of Teams From 1999-2007','Average DPG','def_graph',sort_list_def[-1][0]))
        team_def.close()
                          
        

main()
        

            