
//just some resizing stuff for when page gets small
/*
var wisBig = true; 
if( $(".main").width() < 800 ){
    $(".gtable").css("border-spacing","5px");
    wisBig = false;
}

var changeTableSpacing = function(){
   
    if( wisBig == true){
	if ( $( ".main" ).width() < 800 ){
	    $(".gtable").css("border-spacing","5px");
	    wisBig = false;
	}
    } else if ( $(".main").width() > 800){
	$(".gtable").css("border-spacing","30px");
	wisBig = true;
    }

}

$( window ).resize();

*/

function getThumbs() {
    console.log('getThumbs');
    $.ajax({
	url: '/getall',
	data: window.location.pathname,
	type: 'POST',
	success: function(e) {
	    var paths=JSON.parse(e);
	    $(".main").append("<center><table class='gtable'></table>");
	    row = 0;
	    count = 0;
	    for(i in paths){
		if(count % 3 == 0){
		    $(".gtable").append("<tr id='r" + row.toString() + "'>");
		};
		var img = new Image();
		img.src = paths[i]['thumbnailpath'];
		img.alt = paths[i]['title'];
		img.onclick=function(){
		    $(".gradientBox").attr("visibility","visible");
		    $("#currentImg").attr("src",paths[i]['imagepath']);
		    $("#name").text(paths[i]['title']);
		    $("#code").text(paths[i]['codepath']);
		    if(count > 0 && count < paths.length - 1){
			$("#leftA").click(function(){
			    $("#currentImg").attr("src",paths[i-1]['imagepath']);
			    $("#name").text(paths[i-1]['title']);
			    $("#code").text(paths[i-1]['codepath']);
			});
			$("#rightA").click(function(){
			    $("#currentImg").attr("src",paths[i+1]['imagepath']);
			    $("#name").text(paths[i+1]['title']);
			    $("#code").text(paths[i+1]['codepath']);
			});
		    };
		    if(count == 0){
			$("#rightA").click(function(){
			    $("#currentImg").attr("src",paths[i+1]['imagepath']);
			    $("#name").text(paths[i+1]['title']);
			    $("#code").text(paths[i+1]['codepath']);
			});
		    };
		    if(count == paths.length -1){
			$("#leftA").click(function(){
			    $("#currentImg").attr("src",paths[i-1]['imagepath']);
			    $("#name").text(paths[i-1]['title']);
			    $("#code").text(paths[i-1]['codepath']);
			});
		    };
		};
		console.log(i);
		$("#r" + row.toString()).append("<td id='" + count.toString() + "'>");
		document.getElementById(count.toString()).appendChild(img);
		$("#r" + row.toString()).append("<div class='imgTitle'>" + img.alt + "</div>");
		$("#r" + row.toString()).append("</td>");
		count++;
		if(count % 3 == 0){
		    row++;
		    console.log(count);
		    $(".gtable").append("</tr>");
		};
	    }
	    if(count % 3 != 0){
		$(".gtable").append("</tr>");
	    };
	    $(".gtable").append("</table></center>");
	},
	error: function(error) {
	    console.log(error);
	}
    });
};

window.onload = getThumbs();
