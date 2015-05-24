$(function () {

    $().ready(function () {

        // Build the chart
        $('#stl_blk_graph').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Count of High Performers in Defence From 1999-2007'
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
                data: [['Old Seasons', 512], ['New Seasons', 452]]
            }]
        });
    });

    });