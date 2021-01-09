
        // 基于准备好的dom，初始化echarts实例
        var history_data = echarts.init(document.getElementById('history_chart'));

temp_option = {
    title: {
        text: '实时温度变化',
    },
    tooltip: {
        trigger: 'axis'
    },
    xAxis:  {
        type: 'category',
        boundaryGap: false,
        data: ['周一','周二','周三','周四','周五','周六','周日']
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            formatter: '{value} °C'
        }
    },
    series: [
        {
            name:'最高气温',
            type:'line',
            data:[11, 11, 15, 13, 12, 13, 10],
        }
    ]
};





history_data.setOption(temp_option);
// smoke.setOption(toption);
// people.setOption(toption);



