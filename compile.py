import os
import shutil
import time

import opengl
import shared

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
  d.append(dirpath)
  for file in filenames:
    if file[0] == '.':
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
print "Done."

unhandled_commands = opengl.commands_version_flat.keys()

def spew_category(name, commands):
  commands.sort()

  api_commands = ""
  commands_list = ""
  category_versions = []
  for command in commands:
    versions_available = opengl.commands_version_flat[command]
    versions_available.sort()
    
    classes = "command"
    for v in versions_available:
      classes += " gl" + v.replace(".", "")
      
      if not v in category_versions:
        category_versions.append(v)
        
    latest_present = versions_available[-1][0]
      
    commands_list += "<li class='" + classes + "'><a href='../" + latest_present + "/" + command + "'>" + command + "</a></li>"
    
    if commands != unhandled_commands:
      try:
        unhandled_commands.remove(command)
      except:
        pass

  classes = "category"
  for v in category_versions:
    classes += " gl" + v.replace(".", "")
    
  api_commands += "<li class='" + classes + "'>" + name + ""
  
  api_commands += "<ul>" + commands_list + "</ul></li>"

  return api_commands

api_commands = ""
for category in opengl.command_categories:
  api_commands += spew_category(category, opengl.command_categories[category])

api_commands += spew_category("Uncategorized", unhandled_commands)

header = header.replace("{$api_commands}", api_commands)
footer = footer.replace("{$gentime}", time.strftime("%d %B %Y at %H:%M:%S GMT", time.gmtime()));

version_numbers = opengl.version_commands.keys()

major_versions = opengl.get_major_versions(opengl.version_commands.keys())

for version in major_versions:
  if int(version) < 2:
    continue
    
  written = 0
 
  print "Compiling GL" + version + " ..."
  
  header_for_version = header;
  footer_for_version = footer;
  
  all_versions = opengl.version_commands.keys()
  all_versions.sort()

  # Find latest minor version for this major version.
  latest_minor = version + ".0"
  for version_option in all_versions:
    if latest_minor[0] == version_option[0] and float(latest_minor) < float(version_option):
      latest_minor = version_option
  
  toc_versions_options = ""
  for version_option in all_versions:
    if float(version_option) < 2.1:
      continue

    selected = ""
    if version_option == latest_minor:
      selected = " selected='selected'"
    toc_versions_options = toc_versions_options + "<option value='gl" + version_option.replace(".", "") + "'" + selected + ">GL" + version_option + "</option>"
  header_for_version = header_for_version.replace("{$versions_options}", toc_versions_options)
  header_for_version = header_for_version.replace("{$current_api}", "gl" + latest_minor.replace(".", ""))
    
  for command in opengl.commands_version_flat:
    if not version in opengl.get_major_versions(opengl.commands_version_flat[command]):
      continue
      
    header_for_command = header_for_version
    footer_for_command = footer_for_version

    command_major_versions = opengl.get_major_versions_available(command)
    
    command_versions = "<strong>OpenGL " + version + "</strong>"
    for version_option in command_major_versions:
      if version_option[0] == version[0]:
        continue
        
      command_versions = command_versions + " | <a href='../" + version_option[0] + "/" + command + "'>GL" + version_option[0] + "</a>"
      
    header_for_command = header_for_command.replace("{$command_versions}", command_versions)
    header_for_command = header_for_command.replace("{$title}", command)
    
    improvepage = "Think you can improve this page? <a href='https://github.com/BSVino/docs.gl/blob/master/gl" + version[0] + "/" + command + ".xhtml'>Edit this page</a> on <a href='https://github.com/BSVino/docs.gl/'>GitHub</a>."
    footer_for_command = footer_for_command.replace("{$improvepage}", improvepage)

    version_dir = version[0]
    
    create_directory(output_dir + version_dir)

    command_file = shared.find_command_file(version[0], command)
    if command_file == False:
      raise IOError("Couldn't find page for command " + command + " (" + version[0] + ")")

    fp = open(command_file)
    command_html = fp.read().decode('utf8')
    fp.close()
    
    output_html = header_for_command + command_html + footer_for_command

    output = open(output_dir + version_dir + "/" + command, "w")
    output.write(output_html.encode('ascii', 'xmlcharrefreplace'))
    output.close()
    
    written += 1
  
  print "Wrote " + str(written) + " commands for GL" + version[0]

