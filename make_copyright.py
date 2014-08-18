import os

  
  
def make_copyright(folder):
  f = []
  for (dirpath, dirnames, filenames) in os.walk(folder):
    f.extend(filenames)

  for file in f:
    fp = open(folder + "/" + file)
    command = fp.read()
    fp.close()
    
    command = command.replace('<a id="copyright"></a>', '<div id="Copyright">')
    command = command.replace('<a id="Copyright"></a>', '<div id="Copyright">')
    command += "</div>"
    
    fp = open(folder + "/" + file, "w")
    fp.write(command)
    fp.close()

    
make_copyright("es2")
make_copyright("gl2")
make_copyright("gl3")