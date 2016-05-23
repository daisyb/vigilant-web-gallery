
var isHidden = false;
var sNav = document.getElementById("nav-side"); //sidebar
var tNav = document.getElementById("nav-top"); //topbar
var currentPath = window.location.pathname;


// highlights current link in sidebar
var links = sNav.querySelectorAll('a[href="' + currentPath + '"]');
if(links.length > 0 ){
    links[0].parentElement.className="active";     
}

//for collapsable sidebar
var hideBar = function(bar){
    if (bar.className != "hidden"){
	bar.className += "hidden";
    }
}


var showBar = function(bar) {
    bar.className = "";
}

var toggleBar = function(bar){
    if(bar.className == "hidden"){
	showBar(bar);
    } else {
	hideBar(bar);
    }
}

//decides which nav bars to show based on window size


if (document.documentElement.clientWidth > 1300){
    hideBar(tNav); //hides topbar
}

var windowResizeEvent = function(e){
    if(document.documentElement.clientWidth < 1300){
	showBar(tNav); //shows topbar
    } else {
	hideBar(tNav);
	showBar(sNav);
    }
};

window.addEventListener('resize', windowResizeEvent);

