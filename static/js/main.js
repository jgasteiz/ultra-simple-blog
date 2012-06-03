

var SIMPLE_BLOG = (function() {
	var app = {};

	function initListeners() {
		$(".showFormButton").click(function() {
			$(".post").toggle();
			$(".new-entry-actioner").toggle();
			$(".new-entry-container").toggle();
		});
		$(".cancelEditing").click(function() {
			$(".new-entry-container").animate({
				width: 'toggle',
				height: 'toggle'
			}, {
				duration: 100,
				complete: function() {
					$(".new-entry-actioner").show();
				}
			});
		});
		$(".icon-anchor").click(function(e) {
			e.preventDefault();
		})
	}

	app.enableEditing = function(id) {
		$(".new-entry-actioner").toggle();
		$("#post_" + id).toggle();
		$("#form_" + id).toggle();
	};

	app.deleteEntry = function(id) {
		if(confirm("You're about to delete this entry, ¿do you want to continue?")) {
			location.href = "delete_entry/" + id;
		}
	};

	app.init = function() {
		initListeners();
	};

	return app;
})();

$(document).ready(function() {
	SIMPLE_BLOG.init();
});