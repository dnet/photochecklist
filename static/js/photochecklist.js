function confirm_del(evt) {
	if (!confirm('Are you sure you want to delete the selected photo?')) {
		evt.stop();
	}
}

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
		var ul = link.siblings().find(
				function(sibling) { return sibling.tagName.toLowerCase() == 'ul'; });
		var images = ul.childElements().map(Element.firstDescendant);
		if (images.length) {
			options = '';
			for (var i = 0; i < images.length; i++) {
				options += '<option>' + (i + 1) + '</option>';
			}
			$(divid).insert({ bottom: '<form action="" method="post">' +
				'Delete image: <select name="delete">' + options +
				'</select><input type="submit" value="Delete"/>' +
				'<input type="hidden" name="item"/></form>'});
			$$('#' + divid + ' select')[0].parentNode.observe('submit', confirm_del);
		}
		$$('#' + divid + ' input[name=item]').each(
				function(e) { e.value = link.innerHTML; });
	}
	evt.stop();
}

Event.observe(window, 'load', function() {
	var i = 0;
	$$('#checklist a.itemtitle').each(function(link) {
		link.id = 'cl_link' + (i++);
		link.observe('click', linkClick);	
		var ul = link.siblings().find(
				function(sibling) { return sibling.tagName.toLowerCase() == 'ul'; });
		link.parentNode.addClassName(ul.childElements().length ? 'done' : 'todo');
	});
});
