
function getThumbs() {
    console.log('getThumbs');
    $.get('/getsamples', function(e) {
	console.log('getsamples');
	var paths = JSON.parse(e);
	var i = 0;
	for(i in paths)(function(i){
	    var img = new Image();
	    img.src = "../" + paths[i]['path'] + "/thumbnail.png";
	    console.log(paths[i]['gallery']);
	    console.log("Gallery ^");
	    img.alt = paths[i][0];
	    img.onclick = function(){
		var temp = window.location.pathname.split("/");
		var path = "";
		var count = 0;
		while(count < temp.length - 2){
		    path += temp[count];
		};
		path += "/gallery/" + paths[i]['gallery'];
		window.location.replace(path);
	    };
	    console.log(img.src);
	    console.log(paths[i]['gallery']);
	    $(".main").append("<div class='thumbnail' id='d" + i.toString() + "'></div>");
	    document.getElementById("d"+i.toString()).appendChild(img);
	    $("#d" + i.toString()).append("<div class='imgTitle'>" + paths[i]['gallery'] +
					  "</div>");
	})(i);
    });
};


window.onload = getThumbs();
