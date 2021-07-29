import os
import shutil
import time
import sys
import argparse
import re
import zipfile

import opengl
import glsl
import shared
import shared_glsl
import subprocess
import platform
import urllib2

########################## Command Line Arguments ##########################

parser = argparse.ArgumentParser(description="Compile OpenGL documentation, generate a static webpage.")

parser.add_argument('--full', dest='buildmode', action='store_const', const='full', default='fast', help='Full build (Default: fast build)')
parser.add_argument('--local-assets', dest='local_assets', action='store_true', help='Use local JS/Fonts (Default: don\'t use)')

########################## Print  ##########################

args = parser.parse_args()

if args.buildmode == 'full':
  print "FULL BUILD"
  sys.path.append("htmlmin")
  import htmlmin
else:
  print "FAST BUILD"

def create_directory(dir):
  if not os.path.exists(dir):
      os.makedirs(dir)  

########################## Output Directory Selection ########################## 
 
output_dir = "htdocs/"

print "Resetting output dir..."
while os.path.exists(output_dir):
  try:
    shutil.rmtree(output_dir);
  except:
    pass # It gives an error sometimes. If it didn't work try again.

while not os.path.exists(output_dir):    
  try:
    create_directory(output_dir)
  except:
    pass # It gives an error sometimes. If it didn't work try again.
    
########################## Fetch Remote Assets ########################## 

JS_LIBS = [
  ('jquery', 'jquery.min.js', 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/', None),
  ('jqueryui', 'jquery-ui.min.js', 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/', None),
  ('mathjax', 'MathJax.js', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/', '?config=MML_HTMLorMML'),
  (None, 'config/MML_HTMLorMML.js', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/', '?V=2.7.5'),
  (None, 'jax/output/HTML-CSS/jax.js', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/', '?V=2.7.5'),
  (None, 'jax/output/HTML-CSS/fonts/TeX/fontdata.js', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/', '?V=2.7.5')
]

FONTS = [
  ('roboto', 'roboto.woff', 'https://fonts.gstatic.com/s/roboto/v13/2UX7WLTfW3W8TclTUvlFyQ.woff'),
  ('sourcecodepro', 'sourcecodepro.woff', 'https://fonts.gstatic.com/s/sourcecodepro/v5/mrl8jkM18OlOQN8JLgasDxM0YzuT7MdOe03otPbuUS0.woff')
]

if args.local_assets:
  for name, filename, url, suffix in JS_LIBS:
    path = 'html/copy/' + filename
    if not os.path.exists(path):
      dirname = os.path.dirname(path)
      create_directory(dirname)
      url = url + filename + suffix
      with open(path, 'w') as f:
        print "Downloading " + url
        f.write(urllib2.urlopen(url).read())

  for name, filename, url in FONTS:
    path = 'html/copy/' + filename
    if not os.path.exists(path):
      with open(path, 'wb') as f:
        print "Downloading " + url
        f.write(urllib2.urlopen(url).read())

#################### Copy "html/copy" Files To Output Directory ####################

f = []
d = []
for (dirpath, dirnames, filenames) in os.walk("html/copy"):
  dirpath = dirpath[10:]

  if "test" in dirpath:
    continue
    
  d.append(dirpath)
  for file in filenames:
    if file[-3:] != '.js' and file[-4:] != '.css' and file[-4:] != '.png' and file[-5:] != '.html' and file[-5:] != '.woff' and file != 'opensearch.xml':
      continue
    if file == 'Gruntfile.js':
      continue
    f.append(dirpath + "/" + file)
    
for directory in d:
  create_directory(output_dir + directory)
  
for file in f:
  shutil.copy("html/copy/" + file, output_dir + file)
  
print "Copied " + str(len(f)) + " files"
print "Reading templates..."

########################## Select Index.html Template ##########################
#Todo: use one index only
#the header and index is different for each build

index_path = "html/index.html"

################### Open Header, Footer and Search.js template ##################### 
  
#Open Header , Footer and Search.js template files 
header_fp = open("html/header.html")
header = header_fp.read()
header_fp.close()

footer_fp = open("html/footer.html")
footer = footer_fp.read()
footer_fp.close()

search_fp = open("html/docs.gl.search.js")
search = search_fp.read()
search_fp.close()

index_fp = open(index_path)
index = index_fp.read()
index_fp.close()

def replace_js(markup, prefix):
  for name, filename, url, suffix in JS_LIBS:
    if name:
      template = "{$" + name + "}"
      if args.local_assets:
        url = prefix + filename
      else:
        url = url + filename
      if suffix:
        url = url + suffix
      tag = "<script src='" + url + "'></script>"
      markup = markup.replace(template, tag)
  return markup

index = replace_js(index, prefix="./")
header = replace_js(header, prefix="../")

######################## Write Style.css ########################## 

style_fp = open("html/style.css")
style = style_fp.read()
style_fp.close()

for name, filename, url in FONTS:
  template = "{$" + name + "}"
  if args.local_assets:
    url = "./" + filename
  style = style.replace(template, url)

style_fp = open(output_dir + "/style.css", "w")
style_fp.write(style)
style_fp.close()

######################## Get Versions for Index.html ########################## 

#OpenGL
index_commands_version = opengl.commands_version_flat.keys()
index_commands_version.sort()
index_versions_commands = ""

#GLSL
glsl_index_commands_version = glsl.commands_version_flat.keys()
glsl_index_commands_version.sort()
glsl_index_versions_commands = ""

#OpenGL Loop
for command in index_commands_version:

  major_versions = opengl.get_major_versions_available(command)

  aliases = {}
  # Add aliases to this command. Need to do this because ES has glClearDepthf while GL has glClearDepth
  for alias in opengl.aliased_functions[command]:
    if alias == command:
      continue
    if alias in index_commands_version:
      for version in opengl.get_major_versions_available(alias):
        if not version in major_versions:
          major_versions.append(version)
          aliases[version] = alias
          
  # If the command is an alias we've already done it, skip
  if command in opengl.function_aliases and command != opengl.function_aliases[command] and opengl.function_aliases[command] in index_commands_version:
    continue
  
  latest_version = ''
  all_major_versions_available = []
  for version in major_versions:
    if len(latest_version) == 0 or (latest_version[:2] == 'es' and version[:2] == 'gl') or (latest_version[:2] == version[:2] and float(version[2:]) > float(latest_version[2:])):
      latest_version = version

    all_major_versions_available.append(version)

  index_versions_commands += "<span id='command_" + command + "' class='indexcommand"
  versions_added = []
  for version in opengl.commands_version_flat[command]:
    version = version.replace(".", "")
    if version in versions_added:
      continue
    index_versions_commands += " " + version
    versions_added.append(version)

  for alias_version in aliases:
    for version in opengl.commands_version_flat[aliases[alias_version]]:
      version = version.replace(".", "")
      if version in versions_added:
        continue
      index_versions_commands += " " + version
      versions_added.append(version)

  index_versions_commands += "'><span class='commandcolumn'>" + command + "</span>"
  index_versions_commands += "<span class='commandsearch'>"
  index_versions_commands += command
  for alias in opengl.aliased_functions[command]:
    if alias == command:
      continue
    index_versions_commands += " " + alias
  index_versions_commands += "</span>"
  
  all_major_versions = opengl.get_major_versions(opengl.version_commands_flat.keys())
  for version in all_major_versions:
    if int(version[2:3]) < 2:
      continue
    alias = command

    if version in aliases:
      alias = aliases[version]
      
    if version in all_major_versions_available:
      index_versions_commands += "<span class='versioncolumn'><a href='" + version + "/" + alias + "'>" + version + "</a></span>"
    else:
      index_versions_commands += "<span class='versioncolumn disabled'>" + version + "</span>"
  index_versions_commands += "</span>\n"

#GLSL Loop
for command in glsl_index_commands_version:

  major_versions = glsl.get_major_versions_available(command)

  aliases = {}
  # Add aliases to this command. Need to do this because ES has glClearDepthf while GL has glClearDepth
  for alias in glsl.aliased_functions[command]:
    if alias == command:
      continue
    if alias in index_commands_version:
      for version in glsl.get_major_versions_available(alias):
        if not version in major_versions:
          major_versions.append(version)
          aliases[version] = alias
          
  # If the command is an alias we've already done it, skip
  if command in glsl.function_aliases and command != glsl.function_aliases[command] and glsl.function_aliases[command] in glsl_index_commands_version:
    continue
  
  latest_version = ''
  all_major_versions_available = []
  for version in major_versions:
    if len(latest_version) == 0 or (latest_version[:2] == 'el' and version[:2] == 'sl') or (latest_version[:2] == version[:2] and float(version[2:]) > float(latest_version[2:])):
      latest_version = version

    all_major_versions_available.append(version)

  glsl_index_versions_commands += "<span id='command_" + command + "' class='indexcommand"
  versions_added = []
  for version in glsl.commands_version_flat[command]:
    version = version.replace(".", "")
    if version in versions_added:
      continue
    glsl_index_versions_commands += " " + version
    versions_added.append(version)

  for alias_version in aliases:
    for version in glsl.commands_version_flat[aliases[alias_version]]:
      version = version.replace(".", "")
      if version in versions_added:
        continue
      glsl_index_versions_commands += " " + version
      versions_added.append(version)

  glsl_index_versions_commands += "'><span class='commandcolumn'>" + command + "</span>"
  glsl_index_versions_commands += "<span class='commandsearch'>"
  glsl_index_versions_commands += command
  for alias in glsl.aliased_functions[command]:
    if alias == command:
      continue
    glsl_index_versions_commands += " " + alias
  glsl_index_versions_commands += "</span>"
  
  all_major_versions = glsl.get_major_versions(glsl.version_commands_flat.keys())
  for version in all_major_versions:
    if int(version[2:3]) < 3:
      continue
    if version == "sl3":
      continue
    alias = command

    if version in aliases:
      alias = aliases[version]
      
    if version in all_major_versions_available:
      if version[0:2] == "sl":
        glsl_index_versions_commands += "<span class='slversioncolumn'><a href='" + version + "/" + alias + "'>glsl" + version[2:3] + "</a></span>"
      else:
        glsl_index_versions_commands += "<span class='slversioncolumn'><a href='" + version + "/" + alias + "'>glsl-es" + version[2:3] + "</a></span>"
    else:
      if version[0:2] == "sl":
        glsl_index_versions_commands += "<span class='slversioncolumn disabled'>glsl" + version[2:3] + "</span>"
      else:
        glsl_index_versions_commands += "<span class='slversioncolumn disabled'>glsl-es" + version[2:3] + "</span>"
  glsl_index_versions_commands += "</span>\n"

index = index.replace("{$commandlist}", index_versions_commands+glsl_index_versions_commands)

index_fp = open(output_dir + "/index.html", "w")
index_fp.write(index)
index_fp.close()

######################## Get Versions for search.js ##########################

#OpenGL
search_versions_commands = "var search_versions = {"
search_function_aliases = {}

#GLSL
#Append glsl_search_versions_commands to search_versions_commands
glsl_search_versions_commands = ""
glsl_search_function_aliases = {}

#OpenGL Loop
for version in opengl.version_commands:

  if version[0:2] == "gl" and float(version[2:]) < 2.1:
    continue

  if version[0:2] == "es" and float(version[2:]) < 2.0:
    continue

  search_versions_commands += "'" + version + "':["
  
  if not version[:2] in search_function_aliases:
    search_function_aliases[version[:2]] = {}

  included_commands = []

  for command in opengl.version_commands[version]:
    if not command in included_commands:
      included_commands.append(command)

    if command != opengl.version_commands[version][command]:
      search_function_aliases[version[:2]][command] = opengl.version_commands[version][command]
    
  for command in opengl.version_commands_flat[version]:
    if not command in opengl.version_commands[version] and not command in included_commands:
      included_commands.append(command)

  included_commands.sort()
  for command in included_commands:
    search_versions_commands += "'" + command + "',"

  search_versions_commands += "],"

#GLSL Loop
for version in glsl.version_commands:

  if version[0:2] == "sl" and float(version[2:]) < 4.0:
    continue

  if version[0:2] == "el" and float(version[2:]) < 3.0:
    continue

  glsl_search_versions_commands += "'" + version + "':["
  
  if not version[:2] in glsl_search_function_aliases:
    glsl_search_function_aliases[version[:2]] = {}

  included_commands = []

  for command in glsl.version_commands[version]:
    if not command in included_commands:
      included_commands.append(command)

    if command != glsl.version_commands[version][command]:
      glsl_search_function_aliases[version[:2]][command] = glsl.version_commands[version][command]
    
  for command in glsl.version_commands_flat[version]:
    if not command in glsl.version_commands[version] and not command in included_commands:
      included_commands.append(command)

  included_commands.sort()
  for command in included_commands:
    glsl_search_versions_commands += "'" + command + "',"

  glsl_search_versions_commands += "],"

#Merge OpenGL & GLSL commands
search_versions_commands += glsl_search_versions_commands
 
#All commands for both GLSL and GL
search_versions_commands += "'all': ["

#OpenGL Loop
for command in opengl.commands_version:
    
  major_versions = opengl.get_major_versions(opengl.commands_version[command])
  for version in major_versions:
    if int(version[2]) < 2:
      continue
    search_versions_commands += "'" + version[:3] + "/" + command + "',"

#GLSL Loop
for command in glsl.commands_version:

  major_versions = glsl.get_major_versions(glsl.commands_version[command])
  for version in major_versions:
    if int(version[2]) < 3:
      continue
    if version == 'sl3':
      continue

    search_versions_commands += "'" + version[:3] + "/" + command + "',"	
	
#OpenGL	Loop
for command in opengl.commands_version_flat:

  if command in opengl.commands_version:
    continue
  
  major_versions = opengl.get_major_versions(opengl.commands_version_flat[command])
  for version in major_versions:
    if int(version[2]) < 2:
      continue
    search_versions_commands += "'" + version[:3] + "/" + command + "',"

#GLSL Loop
for command in glsl.commands_version_flat:

  if command in glsl.commands_version:
    continue
  major_versions = glsl.get_major_versions(glsl.commands_version_flat[command])
  for version in major_versions:
    if int(version[2]) < 3:
      continue
      
    if version == 'sl3':
      continue
      
    search_versions_commands += "'" + version[:3] + "/" + command + "',"  
  
#Close
search_versions_commands += "]};"

#Start Aliases 
search_versions_commands += "var function_aliases = {"


#OpenGL Aliases
for version in search_function_aliases:

  search_versions_commands += "'" + version + "':{"
  for alias in search_function_aliases[version]:
    search_versions_commands += alias + ":'" + search_function_aliases[version][alias] + "',"
  search_versions_commands += "},"

#GLSL Aliases
for version in glsl_search_function_aliases:

  if version == 'sl3':
    continue
   
  glsl_search_versions_commands += "'" + version + "':{"
  for alias in glsl_search_function_aliases[version]:
    glsl_search_versions_commands += alias + ":'" + glsl_search_function_aliases[version][alias] + "',"
  glsl_search_versions_commands += "},"
  
search_versions_commands += glsl_search_versions_commands+ "};"

search = search.replace("{$search_versions_commands}", search_versions_commands)


search_fp = open(output_dir + "/docs.gl.search.js", "w")
search_fp.write(search)
search_fp.close()

######################## API Display for Header ##########################

search_versions_options = ""

#GLSL Loop
for version_option in glsl.version_commands.keys():

  if version_option[0:2] == "sl" and float(version_option[2:]) < 4.0:
    continue

  if version_option[0:2] == "el" and float(version_option[2:]) < 3.0:
    continue

  if version_option[:2] == 'sl':
    search_versions_options += "<option value='" + version_option + "'" + ">GLSL " + version_option[2:] + "</option>"
  elif version_option[:2] == 'el':
    search_versions_options += "<option value='" + version_option + "'" + ">GLSL ES" + version_option[2:] + "</option>"

#OpenGL Loop
for version_option in opengl.version_commands.keys():

  if version_option[0:2] == "gl" and float(version_option[2:]) < 2.1:
    continue

  if version_option[0:2] == "es" and float(version_option[2:]) < 2.0:
    continue

  if version_option[:2] == 'gl':
    search_versions_options += "<option value='" + version_option + "'" + ">GL" + version_option[2:] + "</option>"
  elif version_option[:2] == 'es':
    search_versions_options += "<option value='" + version_option + "'" + ">GLES" + version_option[2:] + "</option>"

search_versions_options += "<option selected='selected' value='all'" + ">All</option>"

header = header.replace("{$search_versions}", search_versions_options)

unhandled_commands = opengl.commands_version_flat.keys()
glsl_unhandled_commands = glsl.commands_version_flat.keys()

#Ignore unhandled in glsl
#unhandled_commands += glsl_unhandled_commands

######################## Category Function ##########################

def spew_category(name, commands, current_command, api):
  commands.sort()

  api_commands = ""
  commands_list = ""
  category_versions = []
  found_current_command = False
  for command in commands:
    versions_available ={}
    if api == "gl": 
        versions_available = opengl.commands_version_flat[command]
        versions_available.sort()
    if api == "sl": 
        versions_available = glsl.commands_version_flat[command]
        versions_available.sort()   
		
    if command == current_command:
      found_current_command = True
    
    classes = "command"
    if command == current_command:
      classes += " current"
    for v in versions_available:
      classes += " " + v.replace(".", "")
      
      if not v in category_versions:
        category_versions.append(v)
        
    latest_present = versions_available[-1][0:3]
      
    commands_list += "<li><a class='rewritelink " + classes + "'>" + command + "</a></li>"
    if api == "gl": 
        if commands != unhandled_commands:
            try:
                unhandled_commands.remove(command)
            except:
                pass
        
    if api == "sl":
        if commands != glsl_unhandled_commands:
            try:
                glsl_unhandled_commands.remove(command)
            except:
                pass

  classes = "category"
  if found_current_command:
    classes += " open_me"
  for v in category_versions:
    classes += " " + v.replace(".", "")
    
  api_commands += "<li class='" + classes + "'>" + name + ""
  
  api_commands += "<ul>" + commands_list + "</ul></li>"

  return api_commands

footer = footer.replace("{$gentime}", time.strftime("%d %B %Y at %H:%M:%S GMT", time.gmtime()));


#OpenGL
#version_numbers: Unknown purpose
version_numbers = opengl.version_commands.keys()
major_versions = opengl.get_major_versions(opengl.version_commands.keys())

#GLSL
#glsl_version_numbers: Mimic OpenGL in case it has a purpose
glsl_version_numbers = glsl.version_commands.keys()
glsl_major_versions = glsl.get_major_versions(glsl.version_commands.keys())

major_versions += glsl_major_versions

major_versions.sort()    

######################## Where Everything comes together ##########################

for version in major_versions:
  if int(version[2]) < 2:
    continue
  #No GLSL 3 docs 
  if version == 'sl3':
    continue    
	
  written = 0

  print "Compiling " + version + " ..." 
  header_for_version = header;
  footer_for_version = footer;
  
  all_versions = [];
  
  all_versions = opengl.version_commands.keys()
  glsl_all_versions = glsl.version_commands.keys()
  all_versions += glsl_all_versions
    
  all_versions.sort()
  
  # Find latest minor version for this major version.
  latest_minor = version[:3] + ".0"
  for version_option in all_versions:
    if version[:2] != version_option[:2]:
      continue
      
    if latest_minor[2] == version_option[2] and float(latest_minor[2:]) < float(version_option[2:]):
      latest_minor = version_option

  toc_versions_options = ""
  toc_versions_options_gl = ""
  toc_versions_options_es = ""
  toc_versions_options_sl = ""
  toc_versions_options_el = ""
  for version_option in all_versions:
    if version_option[0:2] == "gl" and float(version_option[2:]) < 2.1:
      continue

    if version_option[0:2] == "es" and float(version_option[2:]) < 2.0:
      continue

    if version_option[0:2] == "sl" and float(version_option[2:]) < 4.0:
      continue

    if version_option[0:2] == "el" and float(version_option[2:]) < 3.0:
      continue
      
    selected = ""
    if version_option == latest_minor:
      selected = " selected='selected'"
 
    if version_option[:2] == 'gl':
      toc_versions_options_gl = toc_versions_options_gl + "<option class='versions_option' value='" + version_option.replace(".", "") + "'" + selected + ">OpenGL " + version_option[2:] + "</option>"
    elif version_option[:2] == 'es':
      toc_versions_options_es = toc_versions_options_es + "<option class='versions_option' value='" + version_option.replace(".", "") + "'" + selected + ">OpenGL ES " + version_option[2:] + "</option>"
    elif version_option[:2] == 'sl':
      toc_versions_options_sl = toc_versions_options_sl + "<option class='versions_option' value='" + version_option.replace(".", "") + "'" + selected + ">GLSL " + version_option[2:] + "</option>"
    elif version_option[:2] == 'el':
      toc_versions_options_el = toc_versions_options_el + "<option class='versions_option' value='" + version_option.replace(".", "") + "'" + selected + ">GLSL ES " + version_option[2:] + "</option>"
  
  #Place dropdown in desired order
  toc_versions_options =  toc_versions_options_gl + toc_versions_options_es + toc_versions_options_sl + toc_versions_options_el  
  header_for_version = header_for_version.replace("{$versions_options}", toc_versions_options)
  header_for_version = header_for_version.replace("{$command_major_version}", version[2])
    
  API_type = ""
    
  if version[0:2] == "gl":
    header_for_version = header_for_version.replace("{$api_name}", "OpenGL")
  elif version[0:2] == "es":
    header_for_version = header_for_version.replace("{$api_name}", "OpenGL ES")
  elif version[0:2] == "sl":
    header_for_version = header_for_version.replace("{$api_name}", "GLSL")
  elif version[0:2] == "el":
    header_for_version = header_for_version.replace("{$api_name}", "GLSL ES")
#Hope this works!
  if version[0:2] == "gl" or version[0:2] == "es":
    commands_version_flat = opengl.commands_version_flat
    API_type = "gl"
  if version[0:2] == "sl" or version[0:2] == "el":
    commands_version_flat = glsl.commands_version_flat  
    API_type = "sl"
    
  for command in commands_version_flat:
  
    if API_type == "gl":
        if not version in opengl.get_major_versions(opengl.commands_version_flat[command]):
            continue
    if API_type == "sl":
        if not version in glsl.get_major_versions(glsl.commands_version_flat[command]):
            continue    
 
    header_for_command = header_for_version
    footer_for_command = footer_for_version

    # Find latest version that has this command present.
    latest_version = version[:3] + ".0"
    for version_option in all_versions:
      if version[:2] != version_option[:2]:
        continue
      if API_type == "gl":
          if not command in opengl.version_commands_flat[version_option]:
              continue
      if API_type == "sl":
          if not command in glsl.version_commands_flat[version_option]:
              continue        
      if latest_version[2] == version_option[2] and float(latest_version[2:]) < float(version_option[2:]):
        latest_version = version_option

    api_commands = ""
    glsl_api_commands =""
    #if API_type == "gl":
    for category in opengl.command_categories:
        api_commands += spew_category(category, opengl.command_categories[category], command , "gl" )
    #if API_type == "sl":
    for category in glsl.command_categories:
        glsl_api_commands += spew_category(category, glsl.command_categories[category], command, "sl")        
    #if API_type == "gl":
    if len(unhandled_commands):
        api_commands += spew_category("Uncategorized", unhandled_commands, command,"gl")
    #if API_type == "sl":
    if len(glsl_unhandled_commands):
        glsl_api_commands += spew_category("Uncategorized", glsl_unhandled_commands, command,"sl")

    header_for_command = header_for_command.replace("{$api_commands}", api_commands)
    header_for_command = header_for_command.replace("{$glsl_api_commands}", glsl_api_commands)
       
    header_for_command = header_for_command.replace("{$current_api}", latest_version.replace(".", ""))
    
    command_major_versions ={}
    if API_type == "gl":
        command_major_versions = opengl.get_major_versions_available(command)
        command_major_versions.sort(reverse=True)
    if API_type == "sl":
        command_major_versions = glsl.get_major_versions_available(command)
        command_major_versions.sort(reverse=True)
    
    command_versions = ""

    for major_version in command_major_versions:
      link_class = ""
      if major_version == version:
        link_class = "class='current'"
        
      es = ""
      if major_version[:2] == 'es' or major_version[:2] == 'el':
        es = "ES "

      if major_version[:2] == 'sl' and int(major_version[2:3]) == 3:
        continue
      
      API=""
      if API_type == "sl":
         API="GLSL"
      if API_type == "gl":
         API="OpenGL"
      
      command_versions += "<a " + link_class + " href='../" + major_version + "/" + command + "'>"+API+" " + es + major_version[2] + "</a><br />"
      
    header_for_command = header_for_command.replace("{$command_versions}", command_versions)
    header_for_command = header_for_command.replace("{$command}", command)
    
    editlink = "https://github.com/BSVino/docs.gl/blob/master/" + version + "/" + command + ".xhtml"
    improvepage = "Think you can improve this page? <a href='" + editlink + "'>Edit this page</a> on <a href='https://github.com/BSVino/docs.gl/'>GitHub</a>."
    footer_for_command = footer_for_command.replace("{$improvepage}", improvepage)

    es = ""
    if version[:2] == 'es':
      es = "ES "

    comments = ""
    '''comments = """<div id="outer_disqus_thread">Guidelines for comments:
      <ul>
        <li>Please limit comments to """+API+ " " + es + version[2] + """ """ + command + """.</li>
        <li>Have a question? Try <a href="http://stackoverflow.com/questions/tagged/opengl">Stack Overflow</a> or the <a href="https://www.opengl.org/discussion_boards/forum.php">OpenGL Forums</a>.</li>
        <li>Instead of commenting, consider <a href='""" + editlink + """'>editing this page on GitHub</a> instead.</li>
      </ul>
    <div id="disqus_thread"></div></div><script type="text/javascript">
    var disqus_shortname = 'docsgl';
    var disqus_identifier = '""" + version + "_" + command + """';
    var disqus_title = 'Comments about """ + version + "/" + command + """';
    var disqus_url = 'https://docs.gl/""" + version + "/" + command + """';

    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = 'https://' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>"""'''
    footer_for_command = footer_for_command.replace("{$comments}", comments)

    version_dir = version
    
    create_directory(output_dir + version_dir)

    command_file = {}
    if API_type == "gl":
        command_file = shared.find_command_file(version, command)
    if API_type == "sl":
        command_file = shared_glsl.find_command_file(version, command)
    if command_file == False:
      raise IOError("Couldn't find page for command " + command + " (" + version + ")")

    fp = open(command_file)
    command_html = fp.read()
    fp.close()
    
    if args.buildmode == 'full':
      command_html = command_html.decode('utf8')

    command_html = command_html.replace("{$pipelinestall}", "")
    
    examples_html = ""
    example_functions ={}
    if API_type == "gl":
        example_functions = opengl.example_functions
    if API_type == "sl":
        example_functions = glsl.example_functions
        
    if command in example_functions:
      examples = "<div class='refsect1' id='examples'><h2>Examples</h2>"
      
      examples_done = []
      #change opengl.example_functions to example_functions
      for example in example_functions[command]:
      
        if not version[:3] in example['versions']:
          continue
          
        if example['example'] in examples_done:
          continue
          
        examples_done.append(example['example'])
        
        code={}
        if API_type =="gl":         
            code = opengl.examples[example['example']]['code']
        if API_type =="sl":         
            code = glsl.examples[example['example']]['code']
            
        def replace_alias(matchobj):
          alias = matchobj.groups()[0]
          command = alias
          
          if API_type =="gl":  
            if alias in opengl.function_aliases:
                command = opengl.function_aliases[alias]
          if API_type =="sl":  
            if alias in glsl.function_aliases:
                command = glsl.function_aliases[alias]                

          return "<a href='../" + version_dir + r"/" + command + "'>" + alias + "</a>"

        code = code.replace("\t", "    ")
        code = code.replace("&", "&amp;")
        code = code.replace("<", "&lt;")
        code = code.replace(">", "&gt;")

        code = re.sub(r"\{%([a-zA-Z_][a-zA-Z_0-9]*?)\}", replace_alias, code)

        code = re.sub(r"(?<![a-zA-Z0-9_])(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|size_t|NULL|GLbyte|GLshort|GLint|GLsizei|GLfloat|GLclampf|GLdouble|GLclampd|GLubyte|GLboolean|GLushort|GLuint|GLenum|GLbitfield|GLchar)(?![a-zA-Z0-9_])", r"<span class='ckeyword'>\1</span>", code)
        code = re.sub(r"(GL_[A-Z_0-9]*)", r"<span class='constant'>\1</span>", code)
        code = re.sub(r'(".*?")', r"<span class='codestring'>\1</span>", code)
        code = re.sub(r'(//.*?)\n', r"<span class='codecomment'>\1</span>\n", code)
        
        examples += "<div class='example'>"
        if API_type == "gl":  
            examples += opengl.examples[example['example']]['description']
        if API_type =="sl":  
            examples += glsl.examples[example['example']]['description']            
        examples += "<pre class='programlisting'>"
        examples += code
        examples += "</pre>"
        examples += "</div>"
      examples += "</div>"

      examples_html = examples

    tutorial_functions={}  
    if API_type =="gl":
        tutorial_functions = opengl.tutorial_functions
    if API_type =="sl":
        tutorial_functions = glsl.tutorial_functions
    
    if command in tutorial_functions:
      tutorials = "<div class='refsect1' id='tutorials'><h2>Tutorials</h2><p>"
      
      tutorials_done = []
      
      tutorial_list={}
      if API_type =="gl":
        tutorial_list = opengl.tutorial_functions[command]
        tutorial_list = sorted(tutorial_list, key=lambda tutorial: opengl.tutorials[tutorial['tutorial']]['name'])
      if API_type =="sl":  
        tutorial_list = glsl.tutorial_functions[command]
        tutorial_list = sorted(tutorial_list, key=lambda tutorial: glsl.tutorials[tutorial['tutorial']]['name'])
        
      for tutorial in tutorial_list:
      
        if not version[:3] in tutorial['versions']:
          continue
          
        if tutorial['tutorial'] in examples_done:
          continue
          
        examples_done.append(tutorial['tutorial'])
        if API_type =="gl":          
            tutorials += '<a href="' + opengl.tutorials[tutorial['tutorial']]['link'] + '">' + opengl.tutorials[tutorial['tutorial']]['name'] + "</a><br />"
        if API_type =="sl":
            tutorials += '<a href="' + glsl.tutorials[tutorial['tutorial']]['link'] + '">' + glsl.tutorials[tutorial['tutorial']]['name'] + "</a><br />"
      tutorials += "</p></div>"
      
      examples_html += tutorials

    command_html = command_html.replace("{$examples}", examples_html)

    # Strip 'mml' namespace from MathML tags so that MathJax can find them
    command_html = re.sub(r'<(/?)mml:(.*?)>', r'<\1\2>', command_html)

    output_html = header_for_command + command_html + footer_for_command

    output = open(output_dir + version_dir + "/" + command, "w")
    output_string = output_html
    if args.buildmode == 'full':
      output_string = htmlmin.minify(output_html, remove_comments=True, reduce_boolean_attributes=True, remove_optional_attribute_quotes=False).encode('ascii', 'xmlcharrefreplace')
    output.write(output_string)
    output.close()
    
    written += 1

  if os.path.exists("html/404.html"):
    header_for_page = header_for_version
    footer_for_page = footer_for_version

    api_commands = ""
    glsl_api_commands = ""
 #   if API_type =="gl":
    for category in opengl.command_categories:
       api_commands += spew_category(category, opengl.command_categories[category], "","gl")
 #   if API_type =="sl":
    for category in glsl.command_categories:
      glsl_api_commands += spew_category(category, glsl.command_categories[category], "","sl")
    
 #   if API_type =="gl":      
    if len(unhandled_commands):
      api_commands += spew_category("Uncategorized", unhandled_commands, "","gl")
 #  if API_type =="sl":      
    if len(glsl_unhandled_commands):
      glsl_api_commands += spew_category("Uncategorized", glsl_unhandled_commands, "","sl")
		  
    header_for_page = header_for_page.replace("{$api_commands}", api_commands)
    header_for_page = header_for_page.replace("{$glsl_api_commands}", glsl_api_commands)

    header_for_page = header_for_page.replace("{$current_api}", latest_minor.replace(".", ""))
    header_for_page = header_for_page.replace("{$command_versions}", "")
    header_for_page = header_for_page.replace("{$command}", "Oops! Can't find '<span id='404command'></span>'.")
    footer_for_page = footer_for_page.replace("{$improvepage}", "")

    fp = open("html/404.html")
    notfound_html = fp.read()
    fp.close()
    
    if args.buildmode == 'full':
      notfound_html = notfound_html.decode('utf8')
    
    output_html = header_for_page + notfound_html + footer_for_page

    output = open(output_dir + version + "/404", "w")
    output_string = output_html
    if args.buildmode == 'full':
      output_string = htmlmin.minify(output_html, remove_comments=True, reduce_boolean_attributes=True, remove_optional_attribute_quotes=False).encode('ascii', 'xmlcharrefreplace')
    output.write(output_string)
    output.close()
  
  print "Wrote " + str(written) + " commands for " + version

with zipfile.ZipFile('docs.gl.zip', 'w', compression=zipfile.ZIP_DEFLATED) as docs_gl_zip:
  for dirname, _, files in os.walk('htdocs'):
    for filename in files:
      docs_gl_zip.write(os.path.join(dirname, filename))

shutil.move("docs.gl.zip", "htdocs/") 
