
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

var getThumbs = function getThumbs() {
    console.log('getThumbs');
    $.ajax({
	url: '/getthumbnails',
	data: window.location.pathname,
	type: 'POST',
	success: function(e) {
	    var paths=JSON.parse(e);
	    $(".main").append("<ul>");
	    for(i=0; i<paths.length; i++){
		$(".main").append("<il><img src=" + paths[i] + "></li>");
	    }
	}
	error: function(error) {
	    console.log(error);
	}
    });
};




