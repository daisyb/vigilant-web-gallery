
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
	url: '/getthumbnails',
	data: window.location.pathname,
	type: 'POST',
	success: function(e) {
	    var stuff = [];
	    $.ajax({
		url: '/getthumbnails',
		data: window.location.pathname,
		type: 'POST',
		success: function(q) {
		    stuff = JSON.parse(q);
		}
		error: function(error) {
		    console.log(error);
		}  
	    });
	    var paths=JSON.parse(e);
	    if(stuff.length != paths.length){
		$(".main").append("<ul id='table'></ul>");
		for(i=0; i<paths.length; i++){
		    var img = new Image();
		    img.src = paths[i];
		    img.onclick = function() {
			/*
			  Do the pop-up thing
			  
			*/
		    };
		    document.getElementById("table").appendChild(img);
		}
	    }else{
		console.log("Unequal number of thumbnails to images");
		console.log("Image Call");
		console.log(stuff);
		console.log("Thumbnail Call");
		console.log(JSON.parse(e));
	    }
	}
	error: function(error) {
	    console.log(error);
	}
    });
};

window.onload = getThumbs();
