import os
import shutil
import time
import sys
import argparse
import re

import opengl
import shared

sys.path.append("htmlmin")
import htmlmin

parser = argparse.ArgumentParser(description="Compile OpenGL documentation, generate a static webpage.")

parser.add_argument('--full', dest='buildmode', action='store_const', const='full', default='fast', help='Full build (Default: fast build)')

args = parser.parse_args()

if args.buildmode == 'full':
  print "FULL BUILD"
else:
  print "FAST BUILD"
  
def create_directory(dir):
  if not os.path.exists(dir):
      os.makedirs(dir)

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
    
f = []
d = []
for (dirpath, dirnames, filenames) in os.walk("html/copy"):
  dirpath = dirpath[10:]

  if "test" in dirpath:
    continue
    
  d.append(dirpath)
  for file in filenames:
    if file[-3:] != '.js' and file[-4:] != '.css' and file[-4:] != '.png' and file[-5:] != '.html':
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
header_fp = open("html/header.html")
header = header_fp.read()
header_fp.close()

footer_fp = open("html/footer.html")
footer = footer_fp.read()
footer_fp.close()

search_fp = open("html/docs.gl.search.js")
search = search_fp.read()
search_fp.close()

index_fp = open("html/index.html")
index = index_fp.read()
index_fp.close()
print "Done."

if os.path.exists('html/copy/jquery.min.js'):
  index = index.replace("{$jquery}", "<script src='jquery.min.js'></script>")
else:
  index = index.replace("{$jquery}", "<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'></script>")

if os.path.exists('html/copy/jquery-ui.min.js'):
  index = index.replace("{$jqueryui}", "<script src='jquery-ui.min.js'></script>")
else:
  index = index.replace("{$jqueryui}", '<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>')

index_commands_version = opengl.commands_version_flat.keys()
index_commands_version.sort()
index_versions_commands = ""
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
      index_versions_commands += "<span class='versioncolumn'>&nbsp;</span>"
  index_versions_commands += "<br /></span>\n"

index = index.replace("{$commandlist}", index_versions_commands)

index_fp = open(output_dir + "/index.html", "w")
index_fp.write(index)
index_fp.close()




search_versions_commands = "var search_versions = {"
search_function_aliases = {}
for version in opengl.version_commands:
  if version[0:2] == "gl" and float(version[2:]) < 2.1:
    continue

  if version[0:2] == "es" and float(version[2:]) < 2.0:
    continue

  search_versions_commands += "'" + version + "':["
  
  if not version[:2] in search_function_aliases:
    search_function_aliases[version[:2]] = {}

  for command in opengl.version_commands[version]:
    search_versions_commands += "'" + command + "',"
    if command != opengl.version_commands[version][command]:
      search_function_aliases[version[:2]][command] = opengl.version_commands[version][command]
    
  for command in opengl.version_commands_flat[version]:
    if not command in opengl.version_commands[version]:
      search_versions_commands += "'" + command + "',"

  search_versions_commands += "],"

search_versions_commands += "'all': ["
for command in opengl.commands_version:
  major_versions = opengl.get_major_versions(opengl.commands_version[command])
  for version in major_versions:
    if int(version[2]) < 2:
      continue
    search_versions_commands += "'" + version[:3] + "/" + command + "',"

for command in opengl.commands_version_flat:
  if command in opengl.commands_version:
    continue
  
  major_versions = opengl.get_major_versions(opengl.commands_version_flat[command])
  for version in major_versions:
    if int(version[2]) < 2:
      continue
    search_versions_commands += "'" + version[:3] + "/" + command + "',"
  
search_versions_commands += "]};"

search_versions_commands += "var function_aliases = {"
for version in search_function_aliases:
  search_versions_commands += "'" + version + "':{"
  for alias in search_function_aliases[version]:
    search_versions_commands += alias + ":'" + search_function_aliases[version][alias] + "',"
  search_versions_commands += "},"

search_versions_commands += "};"

search = search.replace("{$search_versions_commands}", search_versions_commands)

search_fp = open(output_dir + "/docs.gl.search.js", "w")
search_fp.write(search)
search_fp.close()

search_versions_options = ""
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

def spew_category(name, commands, current_command):
  commands.sort()

  api_commands = ""
  commands_list = ""
  category_versions = []
  found_current_command = False
  for command in commands:
    versions_available = opengl.commands_version_flat[command]
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
    
    if commands != unhandled_commands:
      try:
        unhandled_commands.remove(command)
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

version_numbers = opengl.version_commands.keys()

major_versions = opengl.get_major_versions(opengl.version_commands.keys())

for version in major_versions:
  if int(version[2]) < 2:
    continue
    
  written = 0

  print "Compiling " + version + " ..."
  
  header_for_version = header;
  footer_for_version = footer;
  
  all_versions = opengl.version_commands.keys()
  all_versions.sort()

  # Find latest minor version for this major version.
  latest_minor = version[:3] + ".0"
  for version_option in all_versions:
    if version[:2] != version_option[:2]:
      continue
      
    if latest_minor[2] == version_option[2] and float(latest_minor[2:]) < float(version_option[2:]):
      latest_minor = version_option

  toc_versions_options = ""
  for version_option in all_versions:
    if version_option[0:2] == "gl" and float(version_option[2:]) < 2.1:
      continue

    if version_option[0:2] == "es" and float(version_option[2:]) < 2.0:
      continue

    selected = ""
    if version_option == latest_minor:
      selected = " selected='selected'"

    if version_option[:2] == 'gl':
      toc_versions_options = toc_versions_options + "<option value='" + version_option.replace(".", "") + "'" + selected + ">GL" + version_option[2:] + "</option>"
    elif version_option[:2] == 'es':
      toc_versions_options = toc_versions_options + "<option value='" + version_option.replace(".", "") + "'" + selected + ">GLES" + version_option[2:] + "</option>"
      
  header_for_version = header_for_version.replace("{$versions_options}", toc_versions_options)
  header_for_version = header_for_version.replace("{$command_major_version}", version[2])
    
  if version[0:2] == "gl":
    header_for_version = header_for_version.replace("{$api_name}", "OpenGL")
  elif version[0:2] == "es":
    header_for_version = header_for_version.replace("{$api_name}", "OpenGL ES")
    
  for command in opengl.commands_version_flat:
    if not version in opengl.get_major_versions(opengl.commands_version_flat[command]):
      continue
 
    header_for_command = header_for_version
    footer_for_command = footer_for_version

    # Find latest version that has this command present.
    latest_version = version[:3] + ".0"
    for version_option in all_versions:
      if version[:2] != version_option[:2]:
        continue
        
      if not command in opengl.version_commands_flat[version_option]:
        continue
        
      if latest_version[2] == version_option[2] and float(latest_version[2:]) < float(version_option[2:]):
        latest_version = version_option

    api_commands = ""
    for category in opengl.command_categories:
      api_commands += spew_category(category, opengl.command_categories[category], command)

    if len(unhandled_commands):
      api_commands += spew_category("Uncategorized", unhandled_commands, command)

    header_for_command = header_for_command.replace("{$api_commands}", api_commands)
    header_for_command = header_for_command.replace("{$current_api}", latest_version.replace(".", ""))

    command_major_versions = opengl.get_major_versions_available(command)
    command_major_versions.sort(reverse=True)
    
    command_versions = ""
      
    for major_version in command_major_versions:
      link_class = ""
      if major_version == version:
        link_class = "class='current'"
        
      if major_version[:2] == 'gl':
        command_versions += "<a " + link_class + " href='../" + major_version + "/" + command + "'>OpenGL " + major_version[2] + "</a><br />"
      elif major_version[:2] == 'es':
        command_versions += "<a " + link_class + " href='../" + major_version + "/" + command + "'>OpenGL ES " + major_version[2] + "</a><br />"
      
    header_for_command = header_for_command.replace("{$command_versions}", command_versions)
    header_for_command = header_for_command.replace("{$command}", command)
    
    improvepage = "Think you can improve this page? <a href='https://github.com/BSVino/docs.gl/blob/master/" + version + "/" + command + ".xhtml'>Edit this page</a> on <a href='https://github.com/BSVino/docs.gl/'>GitHub</a>."
    footer_for_command = footer_for_command.replace("{$improvepage}", improvepage)

    version_dir = version
    
    create_directory(output_dir + version_dir)

    command_file = shared.find_command_file(version, command)
    if command_file == False:
      raise IOError("Couldn't find page for command " + command + " (" + version + ")")

    fp = open(command_file)
    command_html = fp.read()
    fp.close()
    
    if args.buildmode == 'full':
      command_html = command_html.decode('utf8')

    command_html = command_html.replace("{$pipelinestall}", "")
    
    examples_html = ""
    if command in opengl.example_functions:
      examples = "<div class='refsect1' id='examples'><h2>Examples</h2>"
      
      examples_done = []
      
      for example in opengl.example_functions[command]:
      
        if not version[:3] in example['versions']:
          continue
          
        if example['example'] in examples_done:
          continue
          
        examples_done.append(example['example'])
          
        code = opengl.examples[example['example']]['code']
        
        def replace_alias(matchobj):
          alias = matchobj.groups()[0]
          command = alias
          if alias in opengl.function_aliases:
            command = opengl.function_aliases[alias]

          return "<a href='../" + version_dir + r"/" + command + "'>" + alias + "</a>"

        code = re.sub(r"\{%([a-zA-Z_][a-zA-Z_0-9]*?)\}", replace_alias, code).replace("\t", "    ").replace("&", "&amp;")

        code = re.sub(r"(?<![a-zA-Z0-9_])(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|size_t|NULL|GLbyte|GLshort|GLint|GLsizei|GLfloat|GLclampf|GLdouble|GLclampd|GLubyte|GLboolean|GLushort|GLuint|GLenum|GLbitfield|GLchar)(?![a-zA-Z0-9_])", r"<span class='ckeyword'>\1</span>", code)
        code = re.sub(r"(GL_[A-Z_]*)", r"<span class='constant'>\1</span>", code)
        code = re.sub(r'(".*?")', r"<span class='codestring'>\1</span>", code)
        code = re.sub(r'(//.*?)\n', r"<span class='codecomment'>\1</span>\n", code)
        
        examples += "<div class='example'>"
        examples += opengl.examples[example['example']]['description']
        examples += "<pre class='programlisting'>"
        examples += code
        examples += "</pre>"
        examples += "</div>"
      examples += "</div>"

      examples_html = examples

    if command in opengl.tutorial_functions:
      tutorials = "<div class='refsect1' id='tutorials'><h2>Tutorials</h2><p>"
      
      tutorials_done = []
      
      tutorial_list = opengl.tutorial_functions[command]
      tutorial_list = sorted(tutorial_list, key=lambda tutorial: opengl.tutorials[tutorial['tutorial']]['name'])
      
      for tutorial in tutorial_list:
      
        if not version[:3] in tutorial['versions']:
          continue
          
        if tutorial['tutorial'] in examples_done:
          continue
          
        examples_done.append(tutorial['tutorial'])
          
        tutorials += '<a href="' + opengl.tutorials[tutorial['tutorial']]['link'] + '">' + opengl.tutorials[tutorial['tutorial']]['name'] + "</a><br />"
      tutorials += "</p></div>"
      
      examples_html += tutorials

    command_html = command_html.replace("{$examples}", examples_html)

    output_html = header_for_command + command_html + footer_for_command

    output = open(output_dir + version_dir + "/" + command, "w")
    output_string = output_html
    if args.buildmode == 'full':
      output_string = htmlmin.minify(output_html, remove_comments=True, reduce_boolean_attributes=True).encode('ascii', 'xmlcharrefreplace')
    output.write(output_string)
    output.close()
    
    written += 1
  
  print "Wrote " + str(written) + " commands for " + version

