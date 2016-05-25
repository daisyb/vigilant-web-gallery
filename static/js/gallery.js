
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
	    var paths=[{'thumbnailpath':"../static/images/goat.jpg",'title':"goat1"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat2"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat3"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat4"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat5"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat6"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat7"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat8"}]
	    $(".main").append("<table class='gtable'></table>");
	    count = 0;
	    temp = [];
	    for(i in paths){
		var img = new Image();
		img.src = i['thumbnailpath'];
		img.alt = i['title'];
		temp.push(img);
		count++;
		if(count == 3){
		    $(".gtable").append("<tr><td><img src='" + temp[0].src + "'><div class='imgTitle'>" + temp[0].alt + "</div></td>");
		    $(".gtable").append("<td><img src='" + temp[1].src + "'><div class='imgTitle'>" + temp[1].alt + "</div></td>");
		    $(".gtable").append("<td><img src='" + temp[2].src + "'><div class='imgTitle'>" + temp[2].alt + "</div></td></tr>");
		    count = 0;
		    temp = [];
		};
	    }
	    if(temp.length > 0){
		$(".gtable").append("<tr>");
		for(i in temp){
		    $(".gtable").append("<td><img src='" + i.src + "'><div class='imgTitle'>" + i.alt + "</div></td>");
		};
		$(".gtable").append("</tr>");
	    };
	    $(".gtable").append("</table>");
	}
	error: function(error) {
	    console.log(error);
	}
    });
};

window.onload = getThumbs();
