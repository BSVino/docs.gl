# Read the glsl xhtml files and spit out some python code with all of the supported functions in a big list.
# make sure find_glsl.py has created the glsl doc directories

import os
import xml.etree.ElementTree as ET
import shared_glsl
import ntpath

path = os.path.dirname(os.path.abspath(__file__))

sl_extensions =[

'1', '2', '3', '4', 'Coarse', 'Fine', 'Snorm2x16', 'Snorm4x8', '2x16', '4x8', 'Offset', '2x16', '4x8',
]

#versions displayed in tables 
version_check = ['','sl1.10' , 'sl1.20' , 'sl1.30' , 'sl1.40' , 'sl1.50' , 'sl3.30' , 'sl4.00' , 'sl4.10' ,'sl4.20' ,'sl4.30' ,'sl4.40' ,'sl4.50' ]
version_check_el = ['','el1.10' , 'el3.00' , 'el3.10' ]  

#Get versions for GLSL 
def get_versions( path_file ):

  xtree = ET.parse(path_file)
  element = xtree.find('.//div[@id="versions"]')
  table = element[1][0][2]
  test = '\u2714'; #this is the check symbol
  versions = []
  for x in range(1, 13):
    text = table[0][x].text
    if text == test:
      versions.append(version_check[x])
  return versions

#Get version for GLSL ES  
def get_el_versions( path_file ):
  xtree = ET.parse(path_file)
  element = xtree.find('.//div[@id="versions"]')
  table = element[1][0][2]
  test = '\u2714'; #this is the check symbol
  versions = []
  for x in range(1, 4):
    text = table[0][x].text
    if text == test:
      versions.append(version_check_el[x])
      #print "got it in version " + version_check[x]
  return versions 
  
  
  
def test_extensions(gldir, command):
  # See if removing an extension gives us a real entry
  for extension in sl_extensions:
    if command[-len(extension):] == extension:
      command_file = shared_glsl.find_command_file(gldir, command[0:-len(extension)])
      if not command_file == False:
        return command[0:-len(extension)]
        
  return ""

def test_replacements(gldir, command):
  command_docs = test_extensions(gldir, command)

  if (len(command_docs)):
    return command_docs
  
  #GLSL ES tests
  
  #dfdx
  command_test = command.replace("", "x")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test 
  
  #GLSL tests
  
  #dfdx
  command_test = command.replace("y", "x")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test
  
  #dfdy
  for ext in sl_extensions:
    command_test = command.replace("y", "x")
    command_test = command_test.replace(ext, "")
    if not shared_glsl.find_command_file(gldir, command_test) == False:
      return command_test
  
  command_test = command.replace("U", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test
  
  command_test = command.replace("u", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test
  
  command_test = command.replace("imul", "umul")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test
  
  for ext in sl_extensions:
    command_test = command.replace("S", "U")
    command_test = command_test.replace(ext, "")
    if not shared_glsl.find_command_file(gldir, command_test) == False:
      return command_test
  
  #I don't think we need anything under this part for GLSL
  
  # Some commands need just a single letter removed
  command_test = command.replace("I", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("L", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Getn", "Get")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  if command_test != command:
    test = test_extensions(gldir, command_test)
    if len(test):
      return test

  command_test = command.replace("Readn", "Read")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  # Named commands are stored under their non-named equivalents
  command_test = command.replace("NamedFramebuffer", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("NamedFramebuffer", "Buffer")
  if command_test != command:
    test = test_extensions(gldir, command_test)
    if len(test):
      return test

  command_test = command.replace("Named", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  if command_test != command:
    test = test_extensions(gldir, command_test)
    if len(test):
      return test

  command_test = command.replace("Named", "").replace("Data", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Named", "").replace("SubData", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Texture", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("ArrayAttrib", "AttribArray")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("VertexArray", "Bind")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Array", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("ArrayAttribI", "Attrib")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("ArrayAttribL", "Attrib")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  # For glTextureBuffer -> glTexBuffer and glTextureBufferRange -> glTexBufferRange
  command_test = command.replace("ture", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  if command_test != command:
    return test_extensions(gldir, command_test)
    
  command_test = command.replace("ByRegion", "")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test

  return command


#glsl.xml contains only the list of commands

gltree = ET.parse('specs/glsl.xml')
glroot = gltree.getroot()

current_command_list = []
commads = glroot[1];

stored_version_commands = { '' : [ {'':''} ,] }

#load version keys
for x in version_check:
  stored_version_commands[x] = [ {'':''} ,];
for x in version_check_el:
  stored_version_commands[x] = [ {'':''} ,];
  
for command in commads:
  if command.tag != 'command':
    continue
  current_command_list.append(command[0][0].text);
  
support_API = {'el3' , 'sl4' }
# go over all supported API
for api in support_API:
  for command_name in current_command_list:
    path_file = path+"/"+api+"/"+command_name+".xhtml"
    if(os.path.isfile(path_file)):
      versions = []
      if api[0:2] == 'sl': 
        versions = get_versions(path_file)
      if api[0:2] == 'el':
        versions = get_el_versions(path_file)
      for x in range(len(versions)):
        print(command_name)
        stored_version_commands[versions[x]].append({command_name : command_name})            
    else:
      if os.path.exists(api):
        test_extensions(api , command_name )
        command_file = shared_glsl.find_command_file(api, command_name)
        if command_file == False:
          command_docs = test_replacements(api, command_name)
          command_file = shared_glsl.find_command_file(api, command_docs)
          
          if command_file == False:
            print("No command docs file found for " + command_name + " (" + api + ")")
            print(command_name + " does not exist")
            #Todo: Skip ES errors for now
            if api[0:2] != 'el':
              assert(False)
          else:
            versions = []
            if api[0:2] == 'sl':
              versions = get_versions(path+"/"+api+"/"+command_docs+".xhtml")
            if api[0:2] == 'el':
              versions = get_el_versions(path+"/"+api+"/"+command_docs+".xhtml")
            for x in range(len(versions)):
              stored_version_commands[versions[x]].append({command_name : command_docs})

output = open("glsl_spec.py", "w")
output.write("version_commands = {\n")
  
for version in stored_version_commands:
  if version == "":
    continue

  #print version
  output.write("  '" + version[0:5] + "': {\n")
  for x in stored_version_commands[version]:
    mstring = str(x)
    mstring = mstring.replace("{" , "")
    mstring = mstring.replace("}" , "")
    if mstring == "'': ''":
      continue
    output.write("    " +mstring+ ",\n")
  output.write("  },\n")
  
  
  
output.write("}\n")
output.close()