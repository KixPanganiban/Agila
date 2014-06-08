$(function() {
    // personal analytics
    $('#usage-graph-personal').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Daily Power Consumption'
        },
        subtitle: {
            text: 'Aggregate of All Devices'
        },
        xAxis: {
            categories: [
                '6/01/2014',
                '6/02/2014',
                '6/03/2014',
                '6/04/2014',
                '6/05/2014',
                '6/06/2014',
                '6/07/2014'
            ]
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Consumption (kWh)'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:1f} kWh</b></td></tr>',
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
        series: usageGraphPersonal
    });

    //contribution to community
    $('#community-contribution').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: true
        },
        title: {
            text: 'Your Total Consumption Contribution to Community'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
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
            name: 'Energy Consumption Contribution',
            data: [
                ['You', 13.2],
                ['Rest of the Community', 100 - 13.2]
            ]
        }]
    });
    //community's global contribution
    $('#community-contribution-global').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: true
        },
        title: {
            text: 'Your Community\'s Global Contribution'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
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
            name: 'Energy Consumption Contribution',
            data: [
                ['Your Community', 5.2],
                ['Rest of the World', 100 - 5.2]
            ]
        }]
    });
});