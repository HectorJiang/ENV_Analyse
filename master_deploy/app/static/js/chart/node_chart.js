// 基于准备好的dom，初始化echarts实例
var temp = echarts.init(document.getElementById('temp_chart'));
var humd = echarts.init(document.getElementById('humd_chart'));
var smoke = echarts.init(document.getElementById('smoke_chart'));
var people = echarts.init(document.getElementById('people_chart'));
var drop = echarts.init(document.getElementById('drop_chart'));

temp.showLoading(); // 显示加载动画
humd.showLoading(); // 显示加载动画
smoke.showLoading(); // 显示加载动画
people.showLoading(); // 显示加载动画
drop.showLoading(); // 显示加载动画
current.showLoading(); // 显示加载动画
var time = ["","","","","","","","","","","","","","",""];
var temp_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var humd_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var smoke_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var people_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var drop_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

var ip=document.getElementById("ip").getAttribute("ip");

temp.setOption({
tooltip: {
    trigger: 'axis'
},
title:{
text:'实时温度'
},
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: time
    },
    yAxis: {
        boundaryGap: [0, '50%'],
        type: 'value'
    },
    series: [
        {
            name:'温度',
            type:'line',
            smooth:true,
            symbol: 'none',
            stack: 'a',
            areaStyle: {
                normal: {}
            },
            data: temp_data
        }
    ]
});

humd.setOption({
tooltip: {
    trigger: 'axis'
},
title:{
text:'实时湿度'
},
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: time
    },
    yAxis: {
        boundaryGap: [0, '50%'],
        type: 'value'
    },
    series: [
        {
            name:'湿度',
            type:'line',
            smooth:true,
            symbol: 'none',
            stack: 'a',
            areaStyle: {
                normal: {}
            },
            data: humd_data
        }
    ]
});
smoke.setOption({
tooltip: {
    trigger: 'axis'
},
title:{
text:'烟雾监测'
},
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: time
    },
    yAxis: {
       type: 'category',
        boundaryGap: [0, '50%'],
    },
    series: [
        {
            name:'存在烟雾',
            type:'line',
            smooth:true,
            symbol: 'none',
            stack: 'a',
            areaStyle: {
                normal: {}
            },
            data: smoke_data
        }
    ]
});
people.setOption({
tooltip: {
    trigger: 'axis'
},
title:{
text:'行人监测'
},
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: time
    },
    yAxis: {
       type: 'category',
        boundaryGap: [0, '50%'],

    },
    series: [
        {
            name:'行人通过',
            type:'line',
            smooth:true,
            symbol: 'none',
            stack: 'a',
            areaStyle: {
                normal: {}
            },
            data: people_data
        }
    ]
});
drop.setOption({
tooltip: {
    trigger: 'axis'
},
title:{
text:'雨滴监测'
},
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: time
    },
    yAxis: {
       type: 'category',
        boundaryGap: [0, '50%'],
    },
    series: [
        {
            name:'雨滴',
            type:'line',
            smooth:true,
            symbol: 'none',
            stack: 'a',
            areaStyle: {
                normal: {}
            },
            data: drop_data
        }
    ]
});

var update_chart = function (res){
                // 加入数据，并渲染
            temp.hideLoading(); // 隐藏加载动画
            humd.hideLoading(); // 隐藏加载动画
            smoke.hideLoading(); // 隐藏加载动画
            people.hideLoading(); // 隐藏加载动画
            drop.hideLoading(); // 隐藏加载动画
            //prepare data
            // time.push(res.data[0]);
            // temp_data.push(parseFloat(res.data[1]));
            // humd_data.push(parseFloat(res.data[2]));
            // smoke_data.push(parseFloat(res.data[2]));
            // people_data.push(parseFloat(res.data[2]));
            // drop_data.push(parseFloat(res.data[2]));
            if (time.length >= 10){
                time.shift();
                temp_data.shift();
                humd_data.shift();
                smoke_data.shift();
                people_data.shift();
                drop_data.shift();
            }
            temp.setOption({
                xAxis: {
                    data: date
                },
                series: [{
                    name:'温度',
                    data: data1
                }]
            });
            humd.setOption({
                    xAxis: {
                        data: date
                    },
                    series: [{
                        name:'湿度',
                        data: data2
                    }]
                });
            smoke.setOption({
                    xAxis: {
                        data: date
                    },
                    series: [{
                        name:'存在烟雾',
                        data: data3
                    }]
                });
            people.setOption({
                    xAxis: {
                        data: date
                    },
                    series: [{
                        name:'行人通过',
                        data: data4
                    }]
                });
                drop.setOption({
                        xAxis: {
                            data: date
                        },
                        series: [{
                            name:'雨滴',
                            data: data5
                        }]
                    });
                current.setOption({
                        xAxis: {
                            data: date
                        },
                        series: [{
                            name:'电流',
                            data: data6
                        }]
                    });
            }

        $(document).ready(function() {
        namespace = '/get_data';
        var socket = io.connect("ws://"+"127.0.0.1:5000/get_data");
        // 注册connect监听事件，从服务器获取数据
        socket.on('connect',(res)=>{
            console.log(res["current_data"])
            update_chart(res)
        // emit与message用于向具体事件发送信息，可携带数据
        // on监听事件，等待返回结果
        })
        });