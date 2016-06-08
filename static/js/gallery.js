var globalPaths;
var pathIndex;

function getThumbs() {
    console.log('getThumbs');
    $.ajax({
	url: '/getall',
	data: {'gallery':window.location.pathname},
	type: 'POST',
	success: function(e) {
	    var paths=JSON.parse(e);
	    globalPaths = paths;
	    for(i in paths){
		var img = new Image();
		console.log(paths[i]['thumbnailpath']);
		img.src = "../static/" + paths[i]['thumbnailpath'];
		img.alt = paths[i]['title'];
		img.onclick = function(num){
		    return function() {
			num = parseInt(num);
			$(".gradientBox").css("visibility","visible");
			editGradientContents(paths[num]);
			pathIndex = num;
		    }
		}(i)
		console.log(img.src);
		$(".main").append("<div class='thumbnail' id='d" + i.toString() + "'></div>");
		document.getElementById("d"+i.toString()).appendChild(img);
		$("#d" + i.toString()).append("<div class='imgTitle'>" + paths[i]['title'] +
					      "</div>");
	    };
	    jsIsDumb(paths);
	},
	error: function(error) {
	    console.log(error);
	}
    });
};

window.onload = getThumbs();

var codeBttnEvent = function(e){
    var bttn = $("#code")
    if ( bttn.text() == "View Code"){
	$("#currentCode").css("display","inline");
	$("#currentImg").css("display","none");
	bttn.text("View Image");
    } else if (bttn.text() == "View Image"){
	$("#currentCode").css("display","none");
	$("#currentImg").css("display","inline");
	bttn.text("View Code");
    }
};

$("#code").click(codeBttnEvent);

//this makes all the expanded image stuff disapear
$(".gradientBox").click(function(e){
     $(this).css("visibility","hidden");
});
 
//makes sure the above doesn't apply to div children
 $(".gradientBox > .contents").click(function(e){
     e.stopPropagation();
 });

var editGradientContents = function(path){
    imgPath = "../static/" + path['imagepath'] + "?" + new Date().getTime();
    codePath = "../static/" + path['codepath'] + "?" + new Date().getTime();
    imgName = path['title'];

    $("#name").text(imgName);
    $("#currentImg").attr("src",  imgPath);
    $("#currentCode").attr("src", codePath);
}

$("#leftA").click(function(){
    console.log("hello");
    if (pathIndex != 0){
	pathIndex -= 1;
	editGradientContents(globalPaths[pathIndex]);
    }
});

$("#rightA").click(function(){
    if (pathIndex < globalPaths.length -1){
	pathIndex += 1;
	editGradientContents(globalPaths[pathIndex]);
    };
});
