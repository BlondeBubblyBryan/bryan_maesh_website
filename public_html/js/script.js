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