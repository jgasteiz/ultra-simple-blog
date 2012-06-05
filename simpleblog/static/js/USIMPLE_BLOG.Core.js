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
		toggleCreating();
		toggleEditing();
		toggleDeleting();
	}

	/**
	 * Starts listening at click in .toggleCreating elements
	 *
	 * When clicked this elements:
	 *	- messages must disappear.
	 *	- posts must toggle.
	 *	- lines separating posts must toggle.
	 *	- New Entry button and New Entry Form must toggle.
	 *
	 * @method toggleCreating
	 */
	var toggleCreating = function() {
		$(".toggleCreating").click(function() {
			$(".messages").hide();
			$(".post").toggle();
			$(".line").toggle();
			$(".new-entry-actioner").toggle();
			$(".new-entry-container").toggle();
		});
	};

	/**
	 * Starts listening at click in .toggleEditing elements
	 *
	 * When clicked this elements:
	 *	- messages must disappear.
	 *	- main post must toggle.
	 *	- main post editing form must toggle.
	 *	- If is not of his property, he won't be able to edit it.
	 *
	 * @method toggleEditing
	 */
	var toggleEditing = function() {
		$(".toggleEditing").click(function() {
			var id = $(this).attr("id");
			$(".messages").hide();
			$(".new-entry-actioner").toggle();
			$(".post-" + id).toggle();
			$(".form-" + id).toggle();
		});
	};

	/**
	 * Starts listening at click in .toggleDeleting elements
	 *
	 * When clicked this elements:
	 *	- asks if user want to delete an entry.
	 *	- If is not of his property, he won't be able to delete it.
	 *
	 * @method toggleDeleting
	 */
	var toggleDeleting = function() {
		$(".toggleDeleting").click(function() {
			var id = $(this).attr("id");
			if(confirm("You're about to delete this entry, do you want to continue?")) {
				location.href = "delete_entry/" + id;
			}
		});
	};

	return {
		initListeners: initListeners
	};

})(USIMPLE_BLOG);