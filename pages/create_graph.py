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
    
    
def print_graph():
        
        all_data = data.get_all_data('../dataclean.csv')
        header = sorted(list(set(all_data['Season'])))
        data_vals = []
        for season in header:
            
            season_data = map(int,data.get_specific_data(all_data,'Season',season)['AST'])
            avg = sum(season_data)/(float(data.SEASON_LENGTH)*len(season_data))
            data_vals.append(round(avg,2))
        
        open('assists.js','w').write(create_line(data_vals,header))
        
        
            