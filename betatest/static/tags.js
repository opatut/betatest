$.fn.tags = function() {
	$(this).closest('form').submit(function() {
		var value = $(this).closest('form').find('.input-text').val();
		var spinner = $(this).closest('p').next('p').find('span');
		
		var slug = $(this).attr('slug');
		var project_url = "/ajax/add_project_tag/"+slug+"/"+value;
		var url_ = "/ajax/add_user_tag/"+value;
		if(slug)
			url_ = project_url;
		
		spinner.css('display', 'block');	
		
		$.ajax({
			url: $ROOT_PATH + url_,
			success: function(data){
				$(this).find('.tags').replaceWith(data);
			}
		});
		
		spinner.css('display', 'none');
		
		return false;
	});
};

$(document).ready(function() {
	$('.tags').tags();
});
