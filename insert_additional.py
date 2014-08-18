import os

  
  
def insert_additional(folder):
  f = []
  for (dirpath, dirnames, filenames) in os.walk(folder):
    f.extend(filenames)

  for file in f:
    fp = open(folder + "/" + file)
    command = fp.read()
    fp.close()
    
    command = command.replace('<div class="refsect1" id="versions">', '{$pipelinestall}{$examples}\n      <div class="refsect1" id="versions">')
    command = command.replace('</p></div><div class="refsect1"><a id="seealso"></a><h2>See Also</h2><p>', '</p></div>\n        {$pipelinestall}{$examples}\n        <div class="refsect1"><a id="seealso"></a><h2>See Also</h2><p>')
    command = command.replace('</p></div><div class="refsect1" lang="en" xml:lang="en"><a id="seealso"></a><h2>See Also</h2><p>', '</p></div>\n        {$pipelinestall}{$examples}\n        <div class="refsect1" lang="en" xml:lang="en"><a id="seealso"></a><h2>See Also</h2><p>')
    
    fp = open(folder + "/" + file, "w")
    fp.write(command)
    fp.close()

    
insert_additional("es2")
insert_additional("es3")
insert_additional("gl2")
insert_additional("gl3")
insert_additional("gl4")