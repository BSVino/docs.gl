import os
import shutil
import time
import opengl

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

unhandled_commands = opengl.commands_version.keys()

def spew_category(name, commands):
  commands.sort()
  
  api_commands = ""
  commands_list = ""
  category_versions = []
  for command in commands:
    major_versions = opengl.get_major_versions_available(command)
    major_versions.sort()
    
    classes = "command"
    for v in major_versions:
      classes += " gl" + v
      
      if not v in category_versions:
        category_versions.append(v)
        
    latest_present = major_versions[-1][0]
      
    commands_list += "<li class='" + classes + "'><a href='../" + latest_present + "/" + command + "'>" + command + "</a></li>"
    try:
      unhandled_commands.remove(command)
    except:
      pass

  classes = "category"
  for v in category_versions:
    classes += " gl" + v
    
  api_commands += "<li class='" + classes + "'>" + name + ""
  
  api_commands += "<ul>" + commands_list + "</ul></li>"

  return api_commands

api_commands = ""
for category in opengl.command_categories:
  api_commands += spew_category(category, opengl.command_categories[category])

api_commands += spew_category("Uncategorized", unhandled_commands)

header = header.replace("{$api_commands}", api_commands)

for version in opengl.version_commands:
  written = 0
 
  print "Compiling GL" + version[0] + " ..."
  
  header_for_version = header;
  
  all_versions = opengl.version_commands.keys()
  all_versions.sort()
    
  toc_versions_options = ""
  for version_option in all_versions:
    selected = ""
    if version_option[0] == version[0]:
      selected = " selected='selected'"
    toc_versions_options = toc_versions_options + "<option value='gl" + version_option[0] + "'" + selected + ">GL" + version_option[0] + "</option>"
  header_for_version = header_for_version.replace("{$versions_options}", toc_versions_options)
  header_for_version = header_for_version.replace("{$current_api}", "gl" + version[0])
    
  for command in opengl.commands_version:
    if not version in opengl.commands_version[command]:
      continue
      
    header_for_command = header_for_version

    major_versions = opengl.get_major_versions_available(command)
    
    command_versions = "<strong>OpenGL " + version[0] + "</strong>"
    for version_option in major_versions:
      if version_option[0] == version[0]:
        continue
        
      command_versions = command_versions + " | <a href='../" + version_option[0] + "/" + command + "'>GL" + version_option[0] + "</a>"
      
    header_for_command = header_for_command.replace("{$command_versions}", command_versions)
    header_for_command = header_for_command.replace("{$title}", command)

    version_dir = version[0]
    
    create_directory(output_dir + version_dir)
    
    gldir = "gl" + version[0]
    
    fp = open(gldir + "/" + command + ".xhtml")
    command_html = fp.read().decode('utf8')
    fp.close()
    
    output_html = header_for_command + command_html + footer

    output = open(output_dir + version_dir + "/" + command, "w")
    output.write(output_html.encode('ascii', 'xmlcharrefreplace'))
    output.close()
    
    written += 1
  
  print "Wrote " + str(written) + " commands for GL" + version[0]

