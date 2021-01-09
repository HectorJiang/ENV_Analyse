    $(function () {
        $('#selecttime').datetimepicker({
            format:'YYYY-MM-DD'
  }, function(start, end, label) {

  });
    $("#selecttime1").datetimepicker({
        format:'HH:mm:ss'
    });
    $("#selecttime2").datetimepicker({
        format:'HH:mm:ss'
    });

var time_obj = document.getElementById("history_time");
var temp_obj = document.getElementById("history_temp");
var humd_obj = document.getElementById("history_humd");
var drop_obj = document.getElementById("history_drop");
var people_obj = document.getElementById("history_people");
var current_obj = document.getElementById("history_current");
var somke_obj = document.getElementById("history_smoke");

var history_time=eval("("+time_obj.getAttribute("data")+")");
var history_temp_data1=eval("("+temp_obj.getAttribute("data1")+")");
var history_temp_data2=eval("("+temp_obj.getAttribute("data2")+")");
var history_temp_data3=eval("("+temp_obj.getAttribute("data3")+")");
var history_humd_data1=eval("("+humd_obj.getAttribute("data1")+")");
var history_humd_data2=eval("("+humd_obj.getAttribute("data2")+")");
var history_humd_data3=eval("("+humd_obj.getAttribute("data3")+")");
var history_drop_data1=eval("("+drop_obj.getAttribute("data1")+")");
var history_drop_data2=eval("("+drop_obj.getAttribute("data2")+")");
var history_drop_data3=eval("("+drop_obj.getAttribute("data3")+")");
var history_people_data1=eval("("+people_obj.getAttribute("data1")+")");
var history_people_data2=eval("("+people_obj.getAttribute("data2")+")");
var history_people_data3=eval("("+people_obj.getAttribute("data3")+")");
var history_smoke_data1=eval("("+people_obj.getAttribute("data1")+")");
var history_smoke_data2=eval("("+people_obj.getAttribute("data2")+")");
var history_smoke_data3=eval("("+people_obj.getAttribute("data3")+")");
var history_current_data1=eval("("+people_obj.getAttribute("data1")+")");
var history_current_data2=eval("("+people_obj.getAttribute("data2")+")");
var history_current_data3=eval("("+people_obj.getAttribute("data3")+")");


if(history_time.length != 0)
{
    $("#img").hide();
 var history_temp_chart = echarts.init(document.getElementById('history_temp_chart'));
 var history_humd_chart = echarts.init(document.getElementById('history_humd_chart'));
 var history_drop_chart = echarts.init(document.getElementById('history_drop_chart'));
 var history_people_chart = echarts.init(document.getElementById('history_people_chart'));
 var history_current_chart = echarts.init(document.getElementById('history_current_chart'));
 var history_smoke_chart = echarts.init(document.getElementById('history_smoke_chart'));

// 指定图表的配置项和数据
// 使用刚指定的配置项和数据显示图表。
history_temp_chart.setOption({
        tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        data: history_time
    },
    dataZoom:[{
 　　　　type: 'slider',//图表下方的伸缩条
 　　　　show : true, //是否显示
 　　　　realtime : true, //拖动时，是否实时更新系列的视图
 　　　　start : 0, //伸缩条开始位置（1-100），可以随时更改
 　　　　end : 100, //伸缩条结束位置（1-100），可以随时更改
 　　　},{
        type: 'inside',
        start: 50,
        end: 70
    }],
    yAxis: {
        type: 'value'
    },
    legend: {
        data:['temp1','temp2','temp3']
    },
    series: [
        {
            name:'temp1',
            type:'line',
            stack: '总量',
            data:history_temp_data1
        },
        {
            name:'temp2',
            type:'line',
            stack: '总量',
            data:history_temp_data2
        },
        {
            name:'temp3',
            type:'line',
            stack: '总量',
            data:history_temp_data3
        }
    ]

});


history_humd_chart.setOption({
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        data: history_time
    },
    dataZoom:[{
 　　　　type: 'slider',//图表下方的伸缩条
 　　　　show : true, //是否显示
 　　　　realtime : true, //拖动时，是否实时更新系列的视图
 　　　　start : 0, //伸缩条开始位置（1-100），可以随时更改
 　　　　end : 100, //伸缩条结束位置（1-100），可以随时更改
 　　　},{
        type: 'inside',
        start: 50,
        end: 70
    }],
    yAxis: {
        type: 'value'
    },
    legend: {
        data:['humd1','humd2','humd3']
    },
    series: [
        {
            name:'humd1',
            type:'line',
            stack: '总量',
            data:history_humd_data1
        },
        {
            name:'humd2',
            type:'line',
            stack: '总量',
            data:history_humd_data2
        },
        {
            name:'humd3',
            type:'line',
            stack: '总量',
            data:history_humd_data3
        }
    ]

});


history_drop_chart.setOption({
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        data: history_time
    },
    dataZoom:[{
 　　　　type: 'slider',//图表下方的伸缩条
 　　　　show : true, //是否显示
 　　　　realtime : true, //拖动时，是否实时更新系列的视图
 　　　　start : 0, //伸缩条开始位置（1-100），可以随时更改
 　　　　end : 100, //伸缩条结束位置（1-100），可以随时更改
 　　　},{
        type: 'inside',
        start: 50,
        end: 70
    }],
    yAxis: {
        type: 'category'
    },
    legend: {
        data:['drop1','drop2','drop3']
    },
    series: [
        {
            name:'drop1',
            type:'line',
            stack: '总量',
            data:history_drop_data1
        },
        {
            name:'drop2',
            type:'line',
            stack: '总量',
            data:history_drop_data2
        },
        {
            name:'drop3',
            type:'line',
            stack: '总量',
            data:history_drop_data3
        }
    ]
});


history_smoke_chart.setOption({
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        data: history_time
    },
    dataZoom:[{
 　　　　type: 'slider',//图表下方的伸缩条
 　　　　show : true, //是否显示
 　　　　realtime : true, //拖动时，是否实时更新系列的视图
 　　　　start : 0, //伸缩条开始位置（1-100），可以随时更改
 　　　　end : 100, //伸缩条结束位置（1-100），可以随时更改
 　　　},{
        type: 'inside',
        start: 50,
        end: 70
    }],
    yAxis: {
        type: 'category'
    },
    legend: {
        data:['smoke1','smoke2','smoke3']
    },
    series: [
        {
            name:'smoke1',
            type:'line',
            stack: '总量',
            data:history_smoke_data1
        },
        {
            name:'smoke2',
            type:'line',
            stack: '总量',
            data:history_smoke_data2
        },
        {
            name:'smoke3',
            type:'line',
            stack: '总量',
            data:history_smoke_data3
        }
    ]
});

history_people_chart.setOption({
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        data: history_time
    },
    dataZoom:[{
 　　　　type: 'slider',//图表下方的伸缩条
 　　　　show : true, //是否显示
 　　　　realtime : true, //拖动时，是否实时更新系列的视图
 　　　　start : 0, //伸缩条开始位置（1-100），可以随时更改
 　　　　end : 100, //伸缩条结束位置（1-100），可以随时更改
 　　　},{
        type: 'inside',
        start: 50,
        end: 70
    }],
    yAxis: {
        type: 'category'
    },
    legend: {
        data:['people1','people2','people3']
    },
    series: [
        {
            name:'people1',
            type:'line',
            stack: '总量',
            data:history_people_data1
        },
        {
            name:'people2',
            type:'line',
            stack: '总量',
            data:history_people_data2
        },
        {
            name:'people3',
            type:'line',
            stack: '总量',
            data:history_people_data3
        }
    ]
});

  }});
