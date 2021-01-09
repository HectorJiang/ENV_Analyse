var humd = echarts.init(document.getElementById('humd_node_chart'));

humd.showLoading(); // 显示加载动画


var data=[];
var date=[];

var ip=document.getElementById("ip").getAttribute("ip");

function addData(shift) {
	$.post('/humd_node_chart',{"ip":ip}).done(function (d) {
		d=JSON.parse(d);
		time=(d.created_at).split(" ")
		date.push(time[1]);
		data.push(d.humd);
	});
		if (shift) {
			date.shift();
			data.shift();
		}
}

for (var i = 1; i < 10; i++) {
    addData();
}

humd.setOption({
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: date
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
            data: data
        }
    ]
});

setInterval(function (){
	// 加入数据，并渲染
    addData(true);
    humd.hideLoading(); // 隐藏加载动画
    humd.setOption({
        xAxis: {
            data: date
        },
        series: [{
            name:'湿度',
            data: data
        }]
    });
}, 1000);