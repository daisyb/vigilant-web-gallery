
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
	data: {gallery:window.location.pathname},
	type: 'POST',
	success: function(e) {
	    var paths=[{"thumbnailpath":"../static/images/goat.jpg",'title':"goat1"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat2"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat3"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat4"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat5"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat6"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat7"},{'thumbnailpath':"../static/images/goat.jpg",'title':"goat8"}]
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
