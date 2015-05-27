$(function () {
        $('#assists_graph').highcharts({
             chart: {
               type: 'line'
             },
    
            title: {
               text: 'Average APG of Player from 1999-2007'
            },
            subtitle: {
                text: 'www.basketball-reference.com/'
            },
            xAxis: {
    
                plotLines: [{
                    color: '#FF9E28',
                    width: 2,
                    value: 3.5
                }],    
                categories: ['1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07']
            },
            yAxis: {
                title: {
                    text: 'APG'
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
                    data: [1.54, 1.49, 1.45, 1.47, 1.45, 1.41, 1.41, 1.4]
       
                }]
            });
        });