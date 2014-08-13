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
 
  print "Version " + version + " ..."

  for command in opengl.commands_version:
    if not version in opengl.commands_version[command]:
      continue
   
    create_directory(output_dir + version)
    
    gldir = "gl" + version[0]
    
    fp = open(gldir + "/" + command + ".xhtml")
    command_html = fp.read().decode('utf8')
    fp.close()
    
    output_html = header + command_html + footer

    output = open(output_dir + version + "/" + command, "w")
    output.write(output_html.encode('ascii', 'xmlcharrefreplace'))
    output.close()
    
    written += 1
  
  print "Wrote " + str(written) + " commands for version " + version

f = []
for (dirpath, dirnames, filenames) in os.walk("html/copy"):
  f.extend(filenames)

for file in f:
  shutil.copy("html/copy/" + file, output_dir + file)

print "Copied " + str(len(f)) + " files"