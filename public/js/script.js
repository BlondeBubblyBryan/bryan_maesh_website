$("#desktop").click(function(){
 	$(".on-desktop").show();
	$(".on-mobile").hide();
	$(this).css({'background-color': '#5d3edc', 'color': '#fff'});
	$("#mobile").css({'background-color': '#fff', 'color': '#000'});
});

$("#mobile").click(function(){
 	$(".on-desktop").hide();
	$(".on-mobile").show();
	$(this).css({'background-color': '#5d3edc', 'color': '#fff'});
	$("#desktop").css({'background-color': '#fff', 'color': '#000'});
});

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();   
});

//Initialize
var slider = document.getElementById("slider");
var bulletLabel = document.getElementById("bullet-label");
var bullet = document.getElementById("bullet");
var stripeCost = document.getElementById("stripe-cost");
var maeshCost = document.getElementById("maesh-cost");
var costSaved = document.getElementById("cost-saved");
var margin = document.getElementById("margin");

//Slider
$("document").ready(function() {
  $(".slider").rangeslider();
});
$.fn.rangeslider = function(options) {
  var obj = this;
  var defautValue = obj.attr("value");
  obj.wrap("<span class='range-slider'></span>");
  obj.after("<span class='slider-container'><span class='bar'><span></span></span><span class='bar-btn text-blue-darker'><span>0</span></span></span>");
  obj.attr("oninput", "updateSlider(this)");
  updateSlider(this);
  return obj;
};

function updateSlider(passObj) {
  var obj = $(passObj);
  var value = obj.val();
  var min = obj.attr("min");
  var max = obj.attr("max");
  var range = Math.round(max - min);
  var amount = (value - min);
  var percentage = Math.round((value - min) * 100 / range);
  var nextObj = obj.next();
  nextObj.find("span.bar-btn").css("left", percentage-3 + "%");
  nextObj.find("span.bar > span").css("width", percentage + "%");
  nextObj.find("span.bar-btn > span").text("S$"+amount);

  stripeCost.innerHTML = calculateCost(value, $("#stripe-percentage").html(), $("#stripe-fixed").html());
  maeshCost.innerHTML = calculateCost(value, $("#maesh-percentage").html(), $("#maesh-fixed").html());
  costSaved.innerHTML = (stripeCost.innerHTML - maeshCost.innerHTML).toFixed(2);
  margin.innerHTML = ((costSaved.innerHTML / value) * 100).toFixed(1);
  if (!(isFinite(margin.innerHTML))) {
  	margin.innerHTML = "-";
  } else {
  	margin.innerHTML+="%";
  }
};

//Calculate the transaction fees
function calculateCost(orderValue, percentage, fixed) {
	return (orderValue * Number(percentage)/100 + Number(fixed)).toFixed(2);
}


document.querySelector('#prototype-video').playbackRate = 1.5;
document.querySelector('#prototype-video').play();

function navigatePluginPage(path){
  window.location.href = './docs/'+path;
}