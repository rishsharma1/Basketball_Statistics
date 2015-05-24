import sys
sys.path.insert(0,'../')
import data


SOURCE = "www.basketball-reference.com/"
#first colour represents older seasons,
SEASON_COLOUR = ['rgb(124,181,236)','rgb(67,67,72)']
SEASON_COLOUR_TRAN = ['rgba(124,181,236,0.5)','rgba(67,67,72,0.5)']
def create_line(data_vals,header):
    
    title = "Average Player APG From 1999-2007"
    
    graph_str  = "$(function () {"
    graph_str +=     "$('#assists_graph').highcharts({"
    graph_str +=         "chart: {"
    graph_str +=             """type: 'line'"""
    graph_str +=         "},"
    
    graph_str +=         """title: {
                                text: '%s'
                            },"""%(title)
    
    graph_str += """subtitle: {
                        text: '%s'
                        },"""%(SOURCE)
    
    graph_str += """xAxis: {
                        categories: %s
                    },"""%(header)
    
    graph_str += """yAxis: {
                        title: {
                            text: 'APG'
                        }
                    },"""
    
    graph_str += """plotOptions: {
                        line: {
                            dataLabels: {
                                enabled: true
                             },
                             enableMouseTracking: true
                        }
                    },"""
    
    graph_str += """series: [{
                        name: 'Season',
                        data: %s
       
                   }]
                });
            });"""%(data_vals)
    
    return graph_str


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



def create_scatter(data_vals,x,y,text,id):
    
    graph_str = """$(function () {
    $('#%s').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: '%s'
        },
        subtitle: {
            text: '%s'
        },
        xAxis: {
            title: {
                enabled: true,
                text: '%s'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: '%s'
            }
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b>',
                    pointFormat: '{point.x} %s, {point.y} %s'
                }
            }
        },"""%(id,text,SOURCE,x,y,x,y)
        
    graph_str += "series: ["
    
    for (number, key) in enumerate(sorted(data_vals.keys())):
        
        
        
        if number < 4:
            colour = SEASON_COLOUR_TRAN[0]
        else:
            colour = SEASON_COLOUR_TRAN[1]
            
        graph_str += """{name: '%s',
                            color: '%s',
                            data: %s 
                            },"""%(key,colour,data_vals[key])
           
            
    graph_str =  graph_str[:len(graph_str)-1]
    graph_str += """]
                       });
                    });"""
    
    graph_str = graph_str[:len(graph_str)-1]
    graph_str += ";"
    return graph_str


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
    
    
    
def print_graph():
        
        all_data = data.get_all_data('../dataclean.csv')
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
            
            
            

            season_data = data.get_specific_data(all_data,'Season',season)
            season_points = sum(map(int,season_data['PTS']))/float(data.SEASON_LENGTH*len(set(season_data['Tm'])))

            assists = map(int,season_data['AST'])
            season_stl = sum(map(int,season_data['STL']))/float(data.SEASON_LENGTH*len(set(season_data['Tm'])))
            season_blk = sum(map(int,season_data['BLK']))/float(data.SEASON_LENGTH*len(set(season_data['Tm'])))
            season_def = season_stl+season_blk
        
            tov = data.filter_data_bin(season_data,'TOV',(0,2))
        
            stl = data.filter_data_bin(season_data,'STL',(1,10))
            blk = data.filter_data_bin(season_data,'BLK',(1,10))
        
            ast = data.filter_data_bin(season_data,'AST',(5,11))
            inter_tov_ast = set(tov).intersection(ast)
            union_def = list(set(blk).union(stl))
            
        
            avg = sum(assists)/(float(data.SEASON_LENGTH)*len(assists))
            data_vals.append(round(avg,2))
        
            
            if number < 4:
               
                avg_season_pts.append((round(season_points,2), SEASON_COLOUR[0],season))
                avg_season_def.append((round(season_def,2),SEASON_COLOUR[0],season))
                old_season += len(inter_tov_ast)
                old_def += len(union_def)
            else:
                
                avg_season_pts.append((round(season_points,2), SEASON_COLOUR[1],season))
                avg_season_def.append((round(season_def,2),SEASON_COLOUR[1],season))
                
                new_season += len(inter_tov_ast)
                new_def += len(union_def)

            

            

        count_tov_ast.append(['Old Seasons',old_season])
        count_tov_ast.append(['New Seasons',new_season])
        count_def.append(['Old Seasons',old_def])
        count_def.append(['New Seasons',new_def])
        
                
        
        #count_tov_ast = sorted(count_tov_ast, key=lambda x:x[1])
        assists = open('assists.js','w')
        assists.write(create_line(data_vals,header))
        assists.close()
        
        passing = open('points.js','w')
        passing.write(pie_chart(count_tov_ast,
        'Count of High Performers in Passing From 1999-2007','Count','points_graph'))
        
        passing.close()
        
        sort_list = sorted(avg_season_pts,reverse=True, key= lambda x:x[0])
        
        sort_list_def = sorted(avg_season_def,reverse=True,key = lambda x:x[0])
        
        new_header = [x[2] for x in sort_list]
        new_header_def = [x[2] for x in sort_list_def]
        
        tm_points = open('avg_tm_points.js','w')
        tm_points.write(create_bar(sort_list,new_header,
        'Average PPG of Teams From 1999-2007','Average PPG','bar_graph',sort_list[-1][0]))
        
        tm_points.close()
        
        
        def_count = open('blk_stl_count.js','w')
        def_count.write(pie_chart(count_def,
        'Count of High Performers in Defence From 1999-2007','Count','stl_blk_graph'))
        
        def_count.close()
        
        team_def = open('team_def.js','w')
        team_def.write(create_bar(sort_list_def,new_header_def,
        'Average DPG of Teams From 1999-2007','Average DPG','def_graph',sort_list_def[-1][0]))
                          
        

print_graph()
        
        
            