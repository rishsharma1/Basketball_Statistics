import sys
sys.path.insert(0,'../')
import data


SOURCE = "www.basketball-reference.com/"

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


def pie_chart(data_vals,txt):

    graph_str = """$(function () {

    $('#points_graph').ready(function () {

        // Build the chart
        $('#container').highcharts({
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
                name: 'Count',
                data: %s
            }]
        });
    });

    });"""%(txt,data_vals)

    return graph_str

    
    
def print_graph():
        
        all_data = data.get_all_data('../dataclean.csv')
        header = sorted(list(set(all_data['Season'])))
        data_vals = []
        points_vals = []
        for season in header:
            
            season_data = data.get_specific_data(all_data,'Season',season)
            assists = map(int,season_data['AST'])
            points = map(int,season_data['PTS'])
            avg = sum(assists)/(float(data.SEASON_LENGTH)*len(assists))
            data_vals.append(round(avg,2))
            points_vals.append([season,sum(points)])
        
        
        open('assists.js','w').write(create_line(data_vals,header))
        open('points.js','w').write(pie_chart(points_vals,'Total points for Seasons 1999-2007'))

print_graph()
        
        
            