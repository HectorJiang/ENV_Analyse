setInterval(function (){
	$.post('/').done(function (d) {
		d=JSON.parse(d);
        alert(d);
		document.getElementById("temp").innerHTML = d.temp;
		document.getElementById("humd").innerHTML = d.humd;
		// document.getElementById("people").innerHTML = d.people1;
		// document.getElementById("smoke").innerHTML = d.smoke1;
	});
}, 1000);




