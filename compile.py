import os
import shutil
import time
import opengl

def create_directory(dir):
  if not os.path.exists(dir):
      os.makedirs(dir)

output_dir = "htdocs/"

print "Resetting output dir..."
if os.path.exists(output_dir):
  try:
    shutil.rmtree(output_dir);
  except:
    pass # It gives an error sometimes. If it didn't work it's not a huge deal though.

while not os.path.exists(output_dir):    
  try:
    create_directory(output_dir)
  except:
    pass # It gives an error sometimes. If it didn't work try again/
    
print "Done."

print "Reading templates..."
header_fp = open("html/header.html")
header = header_fp.read()
header_fp.close()

footer_fp = open("html/footer.html")
footer = footer_fp.read()
footer_fp.close()
print "Done."

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
    toc_versions_options = toc_versions_options + "<option" + selected + ">GL" + version_option[0] + "</option>"
  header_for_version = header_for_version.replace("{$versions_options}", toc_versions_options)
    
  for command in opengl.commands_version:
    if not version in opengl.commands_version[command]:
      continue
      
    header_for_command = header_for_version

    versions_available = opengl.commands_version[command]
    versions_available.sort()
    
    major_versions = []
    for v in versions_available:
      major_version = v[0] + ".x"
      if not major_version in major_versions:
        major_versions.append(major_version)
    
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

f = []
for (dirpath, dirnames, filenames) in os.walk("html/copy"):
  f.extend(filenames)

for file in f:
  shutil.copy("html/copy/" + file, output_dir + file)

print "Copied " + str(len(f)) + " files"