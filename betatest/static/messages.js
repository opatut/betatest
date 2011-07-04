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
	});
	
	$("ul.message-list-ul li input.selection").click(function() {
		$(this).attr("checked", !$(this).attr("checked"));
		toggleSelected($(this));
	});
	
});
