import os

def find_command_file(gl_version, command):
  command_file = "gl" + gl_version + "/" + command + ".xhtml"
    
  while not os.path.isfile(command_file):
    if int(gl_version) <= 2:
      return False

    gl_version = str(int(gl_version) - 1)
    command_file = "gl" + gl_version + "/" + command + ".xhtml"
      
  return command_file

