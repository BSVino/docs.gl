{$search_versions_commands}

$(function() {
	search_fn = function(value) {
		version = $("#search_versions").val();
		if (!version || typeof version == 'undefined')
			version = 'all';
			
		if (search_versions[version].indexOf(value) < 0)
			return;

		if (version == 'all')
			window.location.href = "../" + value;
		else
			window.location.href = "../" + version.substring(0, 3) + "/" + value;
	}
	
	$( "#search_button" ).button().click(function(event) {
		search_fn($("#search").val());
	});
	
	$( "#search" ).autocomplete({
		source: search_versions["all"],
		minLength: 3,
		select: function( event, ui ) {
			search_fn(event.target.value);
		},
	});

	$( "#search_versions" ).selectmenu({
		change: function( event, ui ) {
			$("#search").val("");
			$("#search").autocomplete( "option", "source", search_versions[$("#search_versions").val()] );
		},
		width: 70,
	});

	if (typeof $.cookie("api_version") != 'undefined')
		$("#search_versions").val($.cookie("api_version").substring(0, 3) + "." + $.cookie("api_version").substring(3, 4)).selectmenu('refresh');
});