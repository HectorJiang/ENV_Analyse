var smoke = echarts.init(document.getElementById('smoke_node_chart'));

smoke.showLoading(); // 显示加载动画


var data=[];
var date=[];

var ip=document.getElementById("ip").getAttribute("ip");

function addData(shift) {
	$.post('/smoke_node_chart',{"ip":ip}).done(function (d) {
		d=JSON.parse(d);
		time=(d.created_at).split(" ")
		date.push(time[1]);
		data.push(d.smoke);
	});
		if (shift) {
			date.shift();
			data.shift();
		}
}

for (var i = 1; i < 10; i++) {
    addData();
}

smoke.setOption({
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: date
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
            data: data
        }
    ]
});

setInterval(function (){
	// 加入数据，并渲染
    addData(true);
    smoke.hideLoading(); // 隐藏加载动画
    smoke.setOption({
        xAxis: {
            data: date
        },
        series: [{
            name:'存在烟雾',
            data: data
        }]
    });
}, 1000);