
function getThumbs() {
    console.log('getThumbs');
    $.ajax({
	url: '/getall',
	data: {'gallery':window.location.pathname},
	type: 'POST',
	success: function(e) {
	    var paths=JSON.parse(e);
	    for(i in paths){
		var img = new Image();
		console.log(paths[i]['thumbnailpath']);
		img.src = "../static/" + paths[i]['thumbnailpath'];
		img.alt = paths[i]['title'];
		img.onclick=function(){
		    $(".gradientBox").css("visibility","visible");
		    editGradientContents(paths[i]['title'],
					 "../static/" + paths[i]['imagepath'],
					 paths[i]['codepath']); 
		    if(count > 0 && count < paths.length - 1){
			$("#leftA").click(function(){
			    editGradientContents(paths[i-1]['title'],
						 "../static/" + paths[i-1]['imagepath'],
						 paths[i-1]['codepath']);
			});
			$("#rightA").click(function(){
			    editGradientContents(paths[i+1]['title'],
						 "../static/" + paths[i+1]['imagepath'],
						 paths[i+1]['codepath']);
			});
		    };
		    
		    if(count == 0){
			$("#rightA").click(function(){
			    editGradientContents(paths[i+1]['title'],
						 "../static/" + paths[i+1]['imagepath'],
						 paths[i+1]['codepath']);
			});
		    };
		    if(count == paths.length -1){
		    	$("#leftA").click(function(){
			     editGradientContents(paths[i-1]['title'],
						  "../static/" + paths[i-1]['imagepath'],
						  paths[i-1]['codepath']);
		    	});
		    };	
		};
		
		console.log(i);
		console.log(img.src);
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


var editGradientContents = function(imgName, imgPath, codePath){
    $("#name").text(imgName);
    $("#currentImg").attr("src",imgPath);
    $("#currentCode").attr("src",codePath);
}

