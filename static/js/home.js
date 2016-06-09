function getThumbs() {
    console.log('getThumbs');
    $.get('/getsamples', function(e) {
	console.log('getsamples');
	var paths = JSON.parse(e);
	for(i in paths){
	    var img = new Image();
	    img.src = "../static/" + paths[i][1];
	    console.log(paths[i][0]);
	    console.log("Gallery ^");
	    img.alt = paths[i][0];
	    img.onclick = function(){
		var temp = window.location.pathname.split("/");
		var path = "";
		var count = 0;
		while(count < temp.length - 2){
		    path += temp[count];
		};
		path += "/gallery/" + paths[i][0]
		window.location.replace(path);
	    };
	    console.log(img.src);
	    $(".main").append("<div class='thumbnail' id='d" + i.toString() + "'></div>");
	    document.getElementById("d"+i.toString()).appendChild(img);
	    $("#d" + i.toString()).append("<div class='imgTitle'>" + paths[i][0] +
					  "</div>");
	};
    });
};


window.onload = getThumbs();
