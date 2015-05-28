$(function () {
    $('#def_graph').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Average DPG of Teams From 1999-2007'
        },
        subtitle: {
            text: 'www.basketball-reference.com/'
        },
        xAxis: {
            categories: ['1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07'],
            crosshair: true
        },
        yAxis: {
            min: 11,
            title: {
                text: 'Average DPG'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} Average DPG</b></td></tr>',
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
            data:[ {y : 12.82, color: 'rgb(124,181,236)'},{y : 12.17, color: 'rgb(124,181,236)'},{y : 12.39, color: 'rgb(124,181,236)'},{y : 12.5, color: 'rgb(124,181,236)'},{y : 11.4, color: 'rgb(67,67,72)'},{y : 11.24, color: 'rgb(67,67,72)'},{y : 11.16, color: 'rgb(67,67,72)'},{y : 11.39, color: 'rgb(67,67,72)'}]
                
                }, {name: 'New Seasons',
                    data: []
                }]});
          });