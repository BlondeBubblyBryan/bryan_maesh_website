$(document).ready(function(){
	$("#paynow").click(function(){
		$("#paynow").toggleClass("color-select");
		$("#select").toggleClass("disabled");
		$("#circle").toggleClass("far");
		$("#circle").toggleClass("fas");
	});
});