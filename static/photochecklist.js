function linkClick(evt) {
	var link = evt.target;
	var divid = link.id.replace(/link/, 'div');
	var div = $(divid);
	if (div) {
		div.remove();
	} else {
		link.insert({ after: '<div class="pic_upload" id="' + divid + '">' +
			'<form action="" method="post" enctype="multipart/form-data">' +
			'<input type="file" name="file"/><input type="hidden" name="item"/>' +
			'<input type="submit" value="Upload"/></form></div>'});
		$$('#' + divid + ' input[name=item]')[0].value = link.innerHTML;
	}
	evt.stop();
}

Event.observe(window, 'load', function() {
	var i = 0;
	$$('#checklist a').each(function(link) {
		link.id = 'cl_link' + (i++);
		link.observe('click', linkClick);	
	});
});
