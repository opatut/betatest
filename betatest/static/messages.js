// message list selection

function toggleSelected(input) {
	if(input.attr("checked")) {
		input.closest("li").addClass("selected");
	} else {
		input.closest("li").removeClass("selected");
	}
}

$(document).ready(function() {
	$("ul.message-list-ul li").click(function() {
		var $c = $(this).find("input.selection");
		$c.attr("checked", !$c.attr("checked"));
		toggleSelected($c);
	}).dblclick(function() {
		window.location.href = $(this).find("a.message_title").attr("href");
	});
	
	$("ul.message-list-ul li input.selection").click(function() {
		$(this).attr("checked", !$(this).attr("checked"));
		toggleSelected($(this));
	});
	
	$("ul.message-list-ul li input.selection").each(function() {
		toggleSelected($(this));
	});
	
});
