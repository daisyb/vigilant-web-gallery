
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
	data: {gallery:window.location.pathname}
	type: 'POST',
	success: function(e) {
	    var paths=JSON.parse(e);
	    $(".main").append("<table class='gtable'></table>");
	    count = 0;
	    temp = [];
	    for(i in paths){
		var img = new Image();
		img.src = i['thumbnailpath'];
		img.alt = i['title'];
		img.onclick = function() {
		    /*
		      Do the pop-up thing
		      
		    */
		};
		temp.push(img);
		count++;
		if(count == 3){
		    $(".gtable").append("<tr><td><img src='" + temp[0].src + "'><div class='imgTitle'>" + temp[0].alt + "</div></td>");
		    $(".gtable").append("<td><img src='" + temp[1].src + "'><div class='imgTitle'>" + temp[1].alt + "</div></td>");
		    $(".gtable").append("<td><img src='" + temp[2].src + "'><div class='imgTitle'>" + temp[2].alt + "</div></td></tr>");
		    count = 0;
		};
	    }
	    $(".gtable").append("</table>");
	}
	error: function(error) {
	    console.log(error);
	}
    });
};

window.onload = getThumbs();
