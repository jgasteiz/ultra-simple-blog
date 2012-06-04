/**
 * Main class of Ultra Simple Blog - All functions
 *
 * @class Core
 *
 * @author Javi Manzano | @jgasteiz
 */

USIMPLE_BLOG.Core = (function() {

	/**
	 * Init click listeners
	 *
	 * @method initListeners
	 */
	var initListeners = function() {
		$(".showFormButton").click(function() {
			$(".error").hide();
			$(".post").toggle();
			$(".line").toggle();
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

	/**
	 * Enable edit-mode for an entry
	 *
	 * @method enableEditing
	 *
	 * @param {int} id
	 */
	var enableEditing = function(id) {
		$(".error").hide();
		$(".new-entry-actioner").toggle();
		$("#post_" + id).toggle();
		$("#form_" + id).toggle();
	};

	/**
	 * Deletes an entry
	 *
	 * @method deleteEntry
	 *
	 * @param {int} id
	 */
	var deleteEntry = function(id) {
		if(confirm("You're about to delete this entry, do you want to continue?")) {
			location.href = "delete_entry/" + id;
		}
	};

	return {
		initListeners: initListeners,
		enableEditing: enableEditing,
		deleteEntry: deleteEntry
	};

})(USIMPLE_BLOG);