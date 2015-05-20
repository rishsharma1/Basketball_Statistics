$(function () {

    $('#points_graph').ready(function () {

        // Build the chart
        $('#container').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Total points for Seasons 1999-2007'
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
                data: [['1999-00', 223177], ['2000-01', 208964], ['2001-02', 212723], ['2002-03', 213433], ['2003-04', 193523], ['2004-05', 213506], ['2005-06', 219306], ['2006-07', 229389]]
            }]
        });
    });

    });