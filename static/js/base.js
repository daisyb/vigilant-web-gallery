
var isHidden = false;
var sNav = document.getElementById("nav-side"); //sidebar
var tNav = document.getElementById("nav-top"); //topbar
var currentPath = window.location.pathname;

if (currentPath == "/"){
    currentPath = "/home";
}

// highlights current link in sidebar
document.getElementById(currentPath).className = "active";

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
} else {
    //hideBar(sNav);
    showBar(tNav);
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

