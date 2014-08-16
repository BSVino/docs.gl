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

window.last_gl_version = window.current_api.substring(0, 2);
window.api_version = "";

function set_api_version(version) {
	window.api_version = version;
	$.cookie("api_version", version);

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

	if (window.last_gl_version != version.substring(0, 2))
	{
		// Remove functions from GL that ES doesn't have and vice versa.
		hide_commands = function() {
			$(this).addClass("hidden");

			var classList = $(this).attr('class').split(/\s+/);
			for (var i = 0; i < classList.length; i++) {
				if (classList[i].substring(0, 2) === version.substring(0, 2)) {
					$(this).removeClass("hidden");
					break;
				}
			}
		};
		
		$(".command").each(hide_commands);
		$(".category").each(hide_commands);

		$("span.bonsai_inner").trigger('click');
		$("span.bonsai_inner").trigger('click');
		
		window.last_gl_version = version.substring(0, 2);
	}
}

$(function() {
	$( "#command_categories" ).bonsai();
	
	$( "#versions_dropdown" ).selectmenu({
		change: function( event, ui ) {
			set_api_version(ui.item.value);
		}
	});

	if (typeof $.cookie("api_version") != 'undefined')
	{
		set_api_version($.cookie("api_version"));
		$("#versions_dropdown").val($.cookie("api_version")).selectmenu('refresh');
	}
	else
		set_api_version(window.current_api);
	
	$("#style_light").click(function() {
		$("#pagestyle").attr("href", "../style_light.css");
		$.cookie("pagestyle", "light");
	});

	$("#style_dark").click(function() {
		$("#pagestyle").attr("href", "../style_dark.css");
		$.cookie("pagestyle", "dark");
	});
	
	if ($.cookie("pagestyle") == 'light')
		$("#style_light").click();

	if ($.cookie("pagestyle") == 'dark')
		$("#style_dark").click();
		
	$(".open_me span.bonsai_inner").trigger('click');
});