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
	if (name == "el10")
		return "GLSL ES 1.0";
	if (name == "el30")
		return "GLSL ES 3.0";
	if (name == "el31")
		return "GLSL ES 3.1";
	if (name == "sl11")
		return "GLSL 1.1";
	if (name == "sl12")
		return "GLSL 1.2";
	if (name == "sl13")
		return "GLSL 1.3";
	if (name == "sl14")
		return "GLSL 1.4";
	if (name == "sl15")
		return "GLSL 1.5";
	if (name == "sl33")
		return "GLSL 3.3";
	if (name == "sl40")
		return "GLSL 4.0";
	if (name == "sl41")
		return "GLSL 4.1";
	if (name == "sl42")
		return "GLSL 4.2";
	if (name == "sl43")
		return "GLSL 4.3";
	if (name == "sl44")
		return "GLSL 4.4";
	if (name == "sl45")
		return "GLSL 4.5";
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
					
				if (class_api != 'gl' && class_api != 'es' && class_api != 'el' && class_api != 'sl')
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
						
					if (class_api != 'gl' && class_api != 'es' && class_api != 'el' && class_api != 'sl')
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
	$( "#glsl_command_categories" ).bonsai();
	
	$( "#versions_dropdown" ).selectmenu({
		change: function( event, ui ) {
			set_api_version(ui.item.value);
		},
		width: 150
	});

	if (typeof $.cookie("hide_deprecated") != 'undefined')
	{
		window.hide_deprecated = $.cookie("hide_deprecated");
		$('#hide_deprecated').prop('checked', window.hide_deprecated);
	}

	if (typeof $.cookie("api_version") != 'undefined')
	{
		api_version = $.cookie("api_version");

		// We are loading a window.current_api command. If at least the major
		// version matches with that then keep the user setting. Otherwise the
		// name of the GL version won't match the list of functions below it.
		if (api_version.substring(0, 3) == window.current_api.substring(0, 3))
		{
			set_api_version(api_version);
			$("#versions_dropdown").val(api_version).selectmenu('refresh');
		}
		else
		{
			set_api_version(window.current_api);
			$("#versions_dropdown").val(window.current_api).selectmenu('refresh');
		}
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
		var version = 'all';
			
		if (search_versions[version].indexOf(value) < 0){
			return false;
		}
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
		return true;
	}
	
	
	function hide_tooltip (){
		$("#search").trigger('mouseout');
	}
	
	$( "#search_button" ).button().click(function(event) {
		if ( search_fn($("#search").val()) == false){
		
			$("#search").attr("title","");
			$("#search").tooltip();
			$("#search").tooltip( "enable" );
			$("#search").tooltip({ content: "<span style='color:#ff5555' >Command Not Found</span>" });
			$("#search").tooltip({ show: { duration: 100  } });
			$("#search").tooltip({ hide: { duration: 1000  } });
			$("#search").trigger('mouseenter');
			setTimeout(hide_tooltip,800)
			$("#search").tooltip({
				close: function( event, ui ) {
					
						$("#search").tooltip( "disable" );
				}
			});	
		}
		
	});
	
	$( "#search" ).autocomplete({
		source: search_versions["all"],
		minLength: 3,
		select: function( event, ui ) {
			search_fn(event.target.value);
		},
	});

	if (typeof $.cookie("api_version") != 'undefined')
		$("#search").autocomplete( "option", "source", "all" );
	
	$('#hide_deprecated').click(function() {
		window.hide_deprecated = $(this).is(':checked');
		$.cookie("hide_deprecated", window.hide_deprecated, {path: '/'});
		set_api_version(window.api_version);
	});
});
