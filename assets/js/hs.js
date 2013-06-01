$(document).ready(function () {
	// Expand about section click handler
	$('#aboutExpand').click(function() {
		$('#aboutLong').slideDown();
		$('#aboutShort').hide();
	});

	// Hide about section click handler
	$('#aboutHide').click(function() {
		$('#aboutLong').slideUp();
		$('#aboutShort').slideDown();
	});

	// Wizard validate
	$("#findClassBtn").click(function () {
		if ($('input[name=year]:checked').length == 0) {
			$('#wizardError').slideDown();
			return false;
		} else if ($('input[name=experience]:checked').length == 0) {
			$('#wizardError').slideDown();
			return false;
		}
	});

	// Validate rego
	$("#submitRego").click(function () {
		valid = true;
		$.each($('input[type=text]'), function(i, v) {
			if (v.value == '') {
				$('#regoError').slideDown();
				$(v).parent().addClass('error');
				valid = false;
			} else {
				$(v).parent().removeClass('error');
			}
		});
		// scroll to the top so they can see the error message
		if (!valid) {
			$("html, body").animate({ scrollTop: 0 }, 600);
		}
		return valid;
	});
});