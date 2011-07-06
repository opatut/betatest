$.fn.tagsDeleteButtons = function() {
	var spinner = $(this).find('.icon-16-spinner');
	var form = $(this).closest("form");
	var list = $(this);
	
	$(this).find("li").each(function() {
		$(this).find("a.delete").click(function() {
			var tag = $(this).parent().find(".tag").text();
			var href = $(this).attr("href");
			var project_id = form.attr("project_id");		
			var url_ = $ROOT_PATH;
			if(project_id) {
				url_ += "/ajax/remove_project_tag/" + project_id + "/" + tag;
			} else {
				url_ += "/ajax/remove_user_tag/" + tag;
			}
			
			$.ajax({
				url: url_,
				success: function(data){
					new_list = $(data);
					list.replaceWith(new_list);
					new_list.tagsDeleteButtons();
					spinner.fadeOut(200);
				},
				error: function() {
					alert("Ajax error. Redirecting as fallback.");
					window.location = href;
				}
			});
			return false;
		});
	});
};

$.fn.tags = function() {
	var list = $(this);
	
	$(this).closest('form').submit(function() {
		var form = $(this);
		if (form.attr("ajaxerror") == "true") {
			form.attr("ajaxerror", "false");
			return true;
		}
		
		var value = $(this).find('.input-text').val();
		var spinner = $(this).find('.icon-16-spinner');
		
		var project_id = $(this).attr("project_id");
		
		var url_ = $ROOT_PATH;
		if(project_id) {
			url_ += "/ajax/add_project_tag/" + project_id + "/" + value;
		} else {
			url_ += "/ajax/add_user_tag/" + value;
		}
		
		spinner.fadeIn(200);
		$.ajax({
			url: url_,
			success: function(data){
				new_list = $(data);
				list.replaceWith(new_list);
				new_list.tagsDeleteButtons();
				spinner.fadeOut(200);
			},
			error: function() {
				alert("Ajax error. Submitting form as fallback.");
				form.attr("ajaxerror", "true");
				form.submit()
			}
		});
		
		$(this).find('.input-text').val("");
		
		return false;
	});
	list.tagsDeleteButtons();
};

$(document).ready(function() {
	$('.tags').tags();
});
