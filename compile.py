import os
import shutil
import time
import sys
import argparse

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
    if file[-3:] != '.js' and file[-4:] != '.css' and file[-4:] != '.png':
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
print "Done."

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
      classes += " current_command"
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
  latest_minor = version[2] + ".0"
  for version_option in all_versions:
    if latest_minor[0] == version_option[2] and float(latest_minor) < float(version_option[2:]):
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
  header_for_version = header_for_version.replace("{$current_api}", latest_minor.replace(".", ""))
    
  for command in opengl.commands_version_flat:
    if not version in opengl.get_major_versions(opengl.commands_version_flat[command]):
      continue
 
    header_for_command = header_for_version
    footer_for_command = footer_for_version

    api_commands = ""
    for category in opengl.command_categories:
      api_commands += spew_category(category, opengl.command_categories[category], command)

    if len(unhandled_commands):
      api_commands += spew_category("Uncategorized", unhandled_commands, command)

    header_for_command = header_for_command.replace("{$api_commands}", api_commands)

    command_major_versions = opengl.get_major_versions_available(command)
    
    command_versions = '<strong>OpenGL</strong>'
    if version[:2] == 'gl':
      command_versions = "<strong>OpenGL " + version[2] + "</strong>"
    elif version[:2] == 'es':
      command_versions = "<strong>OpenGL ES " + version[2] + "</strong>"
      
    for major_version in command_major_versions:
      if major_version == version:
        continue
        
      if major_version[:2] == 'gl':
        command_versions += " | <a href='../" + major_version + "/" + command + "'>GL" + major_version[2] + "</a>"
      elif major_version[:2] == 'es':
        command_versions += " | <a href='../" + major_version + "/" + command + "'>GLES" + major_version[2] + "</a>"
      
    header_for_command = header_for_command.replace("{$command_versions}", command_versions)
    header_for_command = header_for_command.replace("{$title}", command)
    
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

    output_html = header_for_command + command_html + footer_for_command

    output = open(output_dir + version_dir + "/" + command, "w")
    output_string = output_html
    if args.buildmode == 'full':
      output_string = htmlmin.minify(output_html, remove_comments=True, reduce_boolean_attributes=True, remove_all_empty_space=True).encode('ascii', 'xmlcharrefreplace')
    output.write(output_string)
    output.close()
    
    written += 1
  
  print "Wrote " + str(written) + " commands for " + version

