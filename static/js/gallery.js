var globalPaths;
var pathIndex;

function getThumbs() {
    console.log('getThumbs');
    $.ajax({
	url: '/getall',
	data: {'gallery':window.location.pathname},
	type: 'POST',
	success: function(e) {
	    //gets list of dictionaries with paths, titles, and filetypes for each image
	    var paths=JSON.parse(e);
	    globalPaths = paths;
	    //loops through list 
	    for(i in paths){
		var img = new Image();
		console.log(paths[i]);
		img.src = paths[i]['path'] + "/thumbnail.png";
		img.alt = paths[i]['title'];
		img.onclick = function(num){
		    //onlick edit gradient/box and make visible
		    //opens up slideshow view 
		    return function() {
			num = parseInt(num);
			$(".gradientBox").css("visibility","visible");
			editGradientContents(paths[num]);
			pathIndex = num;
		    }
		}(i)
		console.log(img.src);
		//makes a div with thumbnail and name in it
		//class = thumbnail
		$(".main").append("<div class='thumbnail' id='d" + i.toString() + "'></div>");
		document.getElementById("d"+i.toString()).appendChild(img);
		$("#d" + i.toString()).append("<div class='imgTitle'>" + paths[i]['title'] +
					      "</div>");
	    };
	},
	error: function(error) {
	    console.log(error);
	}
    });
};

window.onload = getThumbs();

//event for clicking 'View Code' button
//switches between displaying code and image
var codeBttnEvent = function(e){
    var bttn = $("#code")
    if ( bttn.text() == "View Code"){
	$("#currentCode").css("display","inline"); //shows code
	$("#currentImg").css("display","none"); //hides image
	bttn.text("View Image"); //changes button text
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

//edits contents of .gradientBox
//puts in proper sources for image and code
//puts in image name
//takes variable path which is the dictionary with paths for specific image
//if i = image index, path = paths[i]
var editGradientContents = function(path){
    imgPath = path['path'] + "/image" + path['filetype'] + "?" + new Date().getTime();
    codePath = path['path'] + "/code.txt" + "?" + new Date().getTime();
    imgName = path['title'];

    $("#name").text(imgName);
    $("#currentImg").attr("src",  imgPath);
    $("#currentCode").attr("src", codePath);
}

//click event for left arrow on slideshow
//loads .gradientBox of image to the left
var leftAEvent = function(){   

    if (pathIndex != 0){
	pathIndex -= 1;
    } else {
	pathIndex = globalPaths.length -1;
    }
    editGradientContents(globalPaths[pathIndex]);
};

//click event for right arrow on slideshow
//loads .gradientBox of image to the right
var rightAEvent= function(){
    if (pathIndex < globalPaths.length -1){
	pathIndex += 1;
    } else {
	pathIndex = 0;
    }
    editGradientContents(globalPaths[pathIndex]);
};

//Binds left and right arrow buttons
$("#leftA").click(leftAEvent);
$("#rightA").click(rightAEvent);

//Binds left and right arrow keys on keyboard
$(document).keydown(function(e){
    if (e.keyCode == 37) { //left key
	leftAEvent();
    } else if (e.keyCode = 39) { //right key
	rightAEvent();
    }

    return false;
});
