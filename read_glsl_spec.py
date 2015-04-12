# Read the glsl xhtml files and spit out some python code with all of the supported functions in a big list.

import os
import xml.etree.ElementTree as ET
import shared_glsl
import ntpath
import codecs

path = os.path.dirname(os.path.abspath(__file__))

sl_extensions =[

'1', '2', '3', '4', 'Coarse', 'Fine', 'Snorm2x16', 'Snorm4x8', '2x16', '4x8', 'Offset', '2x16', '4x8',

]

# imul : umul  , packSnorm4x8 : packUnorm ,   unpackSnorm4x8 : unpackUnorm 

#The table displayed versions
version_check = ['','v1.10' , 'v1.20' , 'v1.30' , 'v1.40' , 'v1.50' , 'v3.30' , 'v4.00' , 'v4.10' ,'v4.20' ,'v4.30' ,'v4.40' ,'v4.50' ]

def get_versions( path_file ):

	xtree = ET.parse(path_file)
	element = xtree.find('.//div[@id="versions"]')
	table = element[1][0][2]
	test = u'\u2714'; #this is the check symbol
	versions = []
	for x in range(1, 13):
		text = table[0][x].text
		if text == test:
			versions.append(version_check[x])
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
  
  command_test = command.replace("imul", "umul")
  if not shared_glsl.find_command_file(gldir, command_test) == False:
    return command_test
  
  for ext in sl_extensions:
	command_test = command.replace("S", "U")
	command_test = command_test.replace(ext, "")
	if not shared_glsl.find_command_file(gldir, command_test) == False:
		return command_test
  
  #I don't think we need anything under this part
  
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


#stored_version_commands = { 'command' : { 'command_docs' : 'command_docs_name' , 'version' : ['v1'] , }, }
#stored_version_commands = {}
#stored_version_commands = { 'version' : { 'command' : 'command_docs' },  }
#stored_version_commands['v1'] = {'abs':'abs'}
stored_version_commands = { '' : [ {'':''} ,] }

for x in version_check:
	stored_version_commands[x] = [ {'':''} ,];

#dic list dic

for command in commads:
	if command.tag != 'command':
		continue
	current_command_list.append(command[0][0].text);

for command_name in current_command_list:
	path_file = path+"\\sl4\\"+command_name+".xhtml"
	if(os.path.isfile(path_file)):
		#print command_name + " exists"
		versions = get_versions(path_file)
		for x in xrange(len(versions)):
			#stored_version_commands[x] = {command_name : command_name}
			stored_version_commands[versions[x]].append({command_name : command_name})
				
			
		#Open File and rack up versions!
	else:
		#print "looking for " +command_name+ "..."
		if os.path.exists("sl4"):
			test_extensions("sl4" , command_name )
			command_file = shared_glsl.find_command_file("sl4", command_name)
			if command_file == False:
				command_docs = test_replacements("sl4", command_name)
				command_file = shared_glsl.find_command_file("sl4", command_docs)
			
				if command_file == False:
					print "No command docs file found for " + command_name + " (" + "sl" + "4" + ")"
					print command_name + " does not exist"
					assert(False)
					#add Test by removing extensions
				else:
					#print "!found " + command_name + " as " +command_docs
					versions = get_versions(path+"\\sl4\\"+command_docs+".xhtml")
					for x in xrange(len(versions)):
					#stored_version_commands[x] = {command_name : command_name}
						 stored_version_commands[versions[x]].append({command_name : command_docs})

	
#print stored_version_commands
		
#stored_version_commands = { 'command' : { 'command_docs' : 'command_docs_name' , 'version' : ['v1'] , }, }
#stored_version_commands = { 'version' : { 'command' : 'command_docs' }, }

#for x in stored_version_commands:
#	print x
#	for y in stored_version_commands[x]:
#		print y

#print stored_version_commands
	
#print	stored_version_commands

output = open("glsl_spec.py", "w")
output.write("version_commands = {\n")
#
#for x in stored_version_commands:
#	output.write(x)
#	for y in stored_version_commands[x]:
#		output.write(y)
	
	
	
	
	
last_api = ""
for version in stored_version_commands:
	print version
		

	#print version
	output.write("  '" + "sl" + version[1:4] + "': {\n")
	#print "  '" + "sl" + version[1:4] + "': {\n"
	for x in stored_version_commands[version]:
		#output.write("    '" + command + "': '" + command_docs + "',\n")
		#output.write("  },\n")
		mstring = str(x)
		mstring = mstring.replace("{" , "")
		mstring = mstring.replace("}" , "")
		if mstring == "'': ''":
			continue
		output.write("    " +mstring+ ",\n")
		#print "    '" + stored_version_commands[version] + "': '" + stored_version_commands[version] + "',\n"
	output.write("  },\n")
output.write("}\n")
output.close()

#  if feature.attrib['api'] == 'gl' or feature.attrib['api'][0:4] == 'gles':
#    gles = feature.attrib['api'][0:4] == 'gles'
  
#output.write("}\n")
#output.close()
  
  
# This wont help because our fake registry doesnt have version!
# we will get the version from the actual table in each xhtml in sl4 dir   
#    gl_prefix = 'gl'
#    if gles:
#      gl_prefix = 'es'
#      
#    if last_api != feature.attrib['api']:
#      current_command_list = []
#      last_api = feature.attrib['api']
#
#    gl_major_version = feature.attrib['number'][0]
#    for child in feature:
#      if child.tag == 'require':
#        if 'profile' in child.attrib and child.attrib['profile'] == 'compatibility':
#          continue
#        for command in child:
#          if command.tag != 'command':
#            continue
#          current_command_list.append(command.attrib['name'])
#      elif child.tag == 'remove':
#        for command in child:
#          if command.tag != 'command':
#            continue
#          current_command_list.remove(command.attrib['name'])
#
#    output.write("  '" + gl_prefix + feature.attrib['number'] + "': {\n")
#    for command in current_command_list:
#      gldir = gl_prefix + gl_major_version
#      
#      command_docs = command
#      
#      # See if the reference file exists on disk
#      if os.path.exists(gldir):
#        command_file = shared.find_command_file(gldir, command)
#        if command_file == False:
#          command_docs = test_replacements(gldir, command)
#
#          command_file = shared.find_command_file(gldir, command_docs)
#        if command_file == False:
#          print "No command docs file found for " + command + " (" + gl_prefix + gl_major_version + ")"
#          output.close()
#          assert(false)
#        
#      output.write("    '" + command + "': '" + command_docs + "',\n")
#    output.write("  },\n")
    
#output.write("}\n")
#output.close()