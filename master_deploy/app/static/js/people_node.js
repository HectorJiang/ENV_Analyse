var people = echarts.init(document.getElementById('people_node_chart'));

people.showLoading(); // 显示加载动画


var data=[];
var date=[];

var ip=document.getElementById("ip").getAttribute("ip");

function addData(shift) {
	$.post('/people_node_chart',{"ip":ip}).done(function (d) {
		d=JSON.parse(d);
		time=(d.created_at).split(" ")
		date.push(time[1]);
		data.push(d.people);
	});
		if (shift) {
			date.shift();
			data.shift();
		}
}

for (var i = 1; i < 10; i++) {
    addData();
}

people.setOption({
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
            name:'行人通过',
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
    people.hideLoading(); // 隐藏加载动画
    people.setOption({
        xAxis: {
            data: date
        },
        series: [{
            name:'行人通过',
            data: data
        }]
    });
}, 1000);