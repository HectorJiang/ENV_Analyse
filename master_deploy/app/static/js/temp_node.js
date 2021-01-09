// 基于准备好的dom，初始化echarts实例
var temp = echarts.init(document.getElementById('temp_chart'));

temp.showLoading(); // 显示加载动画
var time = ["","","","","","","","","","","","","","",""];
var temp_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
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

var update_chart = function (res){
                // 加入数据，并渲染
            temp.hideLoading(); // 隐藏加载动画
            if (time.length >= 10){
                time.shift();
                temp_data.shift();
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