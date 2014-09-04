function gl_printable_name(name) {
	if (name == "es20")
		return "OpenGL ES 2.0";
	if (name == "es30")
		return "OpenGL ES 3.0";
	if (name == "es31")
		return "OpenGL ES 3.1";
	if (name == "gl21")
		return "OpenGL 2.1";
	if (name == "gl30")
		return "OpenGL 3.0";
	if (name == "gl31")
		return "OpenGL 3.1";
	if (name == "gl32")
		return "OpenGL 3.2";
	if (name == "gl33")
		return "OpenGL 3.3";
	if (name == "gl40")
		return "OpenGL 4.0";
	if (name == "gl41")
		return "OpenGL 4.1";
	if (name == "gl42")
		return "OpenGL 4.2";
	if (name == "gl43")
		return "OpenGL 4.3";
	if (name == "gl44")
		return "OpenGL 4.4";
	if (name == "gl45")
		return "OpenGL 4.5";
	return "OpenGL X";
}

window.last_gl_version = "";
window.api_version = "";
window.hide_deprecated = false;
window.last_hide_deprecated = false;

function set_api_version(version) {
	window.api_version = version;
	$.cookie("api_version", version, {path: '/'});

	$( "#opengl_name" ).text(gl_printable_name(version));

	$(".category").addClass("disabled");
	$(".command").addClass("disabled");
	$("." + version).removeClass("disabled");
	
	version_directory = version.substring(0, 3);
	$(".rewritelink").each(function() {
		if ($(this).hasClass(version))
			$(this).attr("href", "../" + version_directory + "/" + $(this).text());
		else
		{
			highest = 0;
			var classList = $(this).attr('class').split(/\s+/);
			for (var i = 0; i < classList.length; i++) {
				class_api = classList[i].substring(0, 2);
				if (class_api != version.substring(0, 2))
					continue;
					
				if (class_api != 'gl' && class_api != 'es')
					continue;

				// Only consider versions <= the one the user has selected.
				if (classList[i].substring(2, 3) <= version.substring(2, 3))
				{
					if (!highest)
						highest = classList[i].substring(2, 3);
						
					if (classList[i].substring(2, 3) > highest)
						highest = classList[i].substring(2, 3);
				}
			}

			if (!highest)
			{
				// No available versions <= the user's choice, so go with the highest one.
				for (var i = 0; i < classList.length; i++) {
					class_api = classList[i].substring(0, 2);
					if (class_api != version.substring(0, 2))
						continue;
						
					if (class_api != 'gl' && class_api != 'es')
						continue;

					if (!highest)
						highest = classList[i].substring(2, 3);
							
					if (classList[i].substring(2, 3) > highest)
						highest = classList[i].substring(2, 3);
				}
			}

			$(this).attr("href", "../" + version.substring(0, 2) + highest + "/" + $(this).text());
		}
	});

	if (window.last_gl_version != version.substring(0, 2) || window.last_hide_deprecated || window.hide_deprecated)
	{
		// Remove functions from GL that ES doesn't have and vice versa.
		hide_commands = function() {
			$(this).addClass("hidden");

			var classList = $(this).attr('class').split(/\s+/);
			if (window.hide_deprecated) {
				for (var i = 0; i < classList.length; i++) {
					if (classList[i] === version) {
						$(this).removeClass("hidden");
						break;
					}
				}
			} else {
				for (var i = 0; i < classList.length; i++) {
					if (classList[i].substring(0, 2) === version.substring(0, 2)) {
						$(this).removeClass("hidden");
						break;
					}
				}
			}
		};
		
		$(".command").each(hide_commands);
		$(".category").each(hide_commands);

		$(".command_categories > li").each(function() {
			var $el = $(this);
			if ($el.hasClass("expanded")) {
				var bonsai = $el.data("bonsai");
				if (bonsai) { bonsai.expand(); }
			}
		});
		
		window.last_gl_version = version.substring(0, 2);
		window.last_hide_deprecated = window.hide_deprecated;
	}
}

$(function() {
	$( "#command_categories" ).bonsai();
	
	$( "#versions_dropdown" ).selectmenu({
		change: function( event, ui ) {
			set_api_version(ui.item.value);
		}
	});

	if (typeof $.cookie("hide_deprecated") != 'undefined')
	{
		window.hide_deprecated = $.cookie("hide_deprecated");
		$('#hide_deprecated').prop('checked', window.hide_deprecated);
	}

	if (typeof $.cookie("api_version") != 'undefined')
	{
		set_api_version($.cookie("api_version"));
		$("#versions_dropdown").val($.cookie("api_version")).selectmenu('refresh');
	}
	else
	{
		set_api_version(window.current_api);
		$("#versions_dropdown").val(window.current_api).selectmenu('refresh');
	}

	$("#style_light").click(function() {
		$("#pagestyle").attr("href", "../style_light.css");
		$.cookie("pagestyle", "light", {path: '/'});
	});

	$("#style_dark").click(function() {
		$("#pagestyle").attr("href", "../style_dark.css");
		$.cookie("pagestyle", "dark", {path: '/'});
	});
	
	if ($.cookie("pagestyle") == 'light')
		$("#style_light").click();

	if ($.cookie("pagestyle") == 'dark')
		$("#style_dark").click();
		
	// hack to run after bonsai is initailized
	setTimeout(function() {
		$(".open_me").each(function() {
			// copied from bonsai js to expand w/o animation
			var listItem = $(this);
			if( !listItem.data('subList') )
				return;
			listItem.addClass('expanded').removeClass('collapsed');
			var subList = $(listItem.data('subList'));
			subList.css('height', 'auto');
		});
	}, 1);
	

	search_fn = function(value) {
		version = $("#search_versions").val();
		if (!version || typeof version == 'undefined')
			version = 'all';
			
		if (search_versions[version].indexOf(value) < 0)
			return;

		var alias_api = version.substring(0, 2);
		var alias = value;
		var directory = version.substring(0, 3) + "/";
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
	
	$('#hide_deprecated').click(function() {
		window.hide_deprecated = $(this).is(':checked');
		$.cookie("hide_deprecated", window.hide_deprecated, {path: '/'});
		set_api_version(window.api_version);
	});
});
