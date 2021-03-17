
//加减class
$(function() {
	$(".nav ul li").click(function(){
		$(this).addClass('cur').siblings().removeClass('cur');
	});
	$(".mainC1 h3 a").click(function(){
		$(this).addClass('cur').siblings().removeClass('cur');
	});
	$(".businessLMain h3").click(function(){
		$(this).addClass('cur').siblings().removeClass('cur');
	});
});