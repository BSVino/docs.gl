import os

def find_command_file(gl_version, command):
  command_file = gl_version + "/" + command + ".xhtml"
    
  while not os.path.isfile(command_file):
    if gl_version[:2] == 'gl' and int(gl_version[2]) <= 2:
      return False
      
    if gl_version[:2] == 'es' and int(gl_version[2]) < 1:
      return False

    gl_version = gl_version[:2] + str(int(gl_version[2]) - 1)
    command_file = gl_version + "/" + command + ".xhtml"
      
  return command_file

