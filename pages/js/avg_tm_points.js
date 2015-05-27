$(function () {
    $('#bar_graph').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Average PPG of Teams From 1999-2007'
        },
        subtitle: {
            text: 'www.basketball-reference.com/'
        },
        xAxis: {
            categories: ['1999-00', '2006-07', '2002-03', '2001-02', '2005-06', '2000-01', '2004-05', '2003-04'],
            crosshair: true
        },
        yAxis: {
            min: 82,
            title: {
                text: 'Average PPG'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} Average PPG</b></td></tr>',
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
            data:[ {y : 95.01, color: 'rgb(124,181,236)'},{y : 94.4, color: 'rgb(67,67,72)'},{y : 90.86, color: 'rgb(124,181,236)'},{y : 90.56, color: 'rgb(124,181,236)'},{y : 90.25, color: 'rgb(67,67,72)'},{y : 88.96, color: 'rgb(124,181,236)'},{y : 87.86, color: 'rgb(67,67,72)'},{y : 82.39, color: 'rgb(67,67,72)'}]
                
                }, {name: 'New Seasons',
                    data: []
                }]});
          });