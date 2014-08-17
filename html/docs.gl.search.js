{$search_versions_commands}

$(function() {
	search_fn = function(value) {
		version = $("#search_versions").val();
		if (!version || typeof version == 'undefined')
			version = 'all';
			
		if (search_versions[version].indexOf(value) < 0)
			return;

		var alias_api = version.substring(0, 2);
		var alias = value;
		var directory = version.substring(0, 3) + "/";
		console.log(alias_api + ":" + alias + ":" + directory);
		if (version == 'all')
		{
			alias_api = value.substring(0, 2);
			alias = value.substring(4);
			directory = value.substring(0, 4);
		}
			
		var command_page = alias;
		if (alias in function_aliases[alias_api])
			command_page = function_aliases[alias_api][alias]

		window.location.href = window.base_directory + directory + command_page;
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
	{
		$("#search_versions").val($.cookie("api_version").substring(0, 3) + "." + $.cookie("api_version").substring(3, 4)).selectmenu('refresh');
		$("#search").autocomplete( "option", "source", search_versions[$("#search_versions").val()] );
	}
});