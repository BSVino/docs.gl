# Read the opengl spec xml files and spit out some python code with all of the supported functions in a big list.

import os
import xml.etree.ElementTree as ET
import shared

extensions = [
  'f', 'i', 'v', 'd', 's', '1', '2', 'x',
  'fv', 'iv', '3b', '3d', '3s', '3i', '3f', '4b', '4s', '4i', '4f', '4d', 'dv', 'sv', '2d', '2f', '2i', '2s', '1d', '1f', '1i', '1s', 'ub', 'fi', '1D', '2D', '3D', '4x', 'xv', '3x',
  '3bv', '3ub', '3us', '3ui', '4ub', '4us', '4ui', '3dv', '3fv', '3iv', '3sv', '4bv', '4dv', '4fv', '4iv', '4sv', '2dv', '2fv', '2iv', '2sv', '1dv', '1fv', '1iv', '1sv', 'uiv', 'usv', 'ubv', 'Iiv', 'I1i', 'I2i', 'I3i', 'I4i', '1ui', '2ui', '3ui', '4ui', 'L1d', 'L2d', 'L3d', 'L4d', 'Ldv', 'i_v',
  '3ubv', '3uiv', '3usv', '3ufv', '4ubv', '4uiv', '4usv', '4ufv', '4Nbv', '4Niv', '4Nsv', '4Nub', '4Nuv', 'Iuiv', 'I1ui', 'I2ui', 'I3ui', 'I4ui', 'I1iv', 'I2iv', 'I3iv', 'I4iv', 'I4bv', 'I4sv', '1uiv', '2uiv', '3uiv', '4uiv', 'i64v', 'P1ui', 'P2ui', 'P3ui', 'P4ui', 'L1dv', 'L2dv', 'L3dv', 'L4dv', '64iv',
  '4Nubv', '4Nuiv', '4Nusv', 'I1uiv', 'I2uiv', 'I3uiv', 'I4uiv', 'I4ubv', 'I4usv', 'ui64v', 'P1uiv', 'P2uiv', 'P3uiv', 'P4uiv', 'i64_v',
  'Booleanv', 'Booleani_v', 'Doublev', 'Doublei_v', 'Floatv', 'Floati_v', 'Integerv', 'Integeri_v',  'Integer64v', 'Integer64i_v', 'Fixedv', 'Matrix2fv', 'Matrix3fv', 'Matrix4fv', 'Matrix2x3fv', 'Matrix3x2fv', 'Matrix2x4fv', 'Matrix4x2fv', 'Matrix3x4fv', 'Matrix4x3fv', 'Matrix2dv', 'Matrix3dv', 'Matrix4dv', 'Matrix2x3dv', 'Matrix3x2dv', 'Matrix2x4dv', 'Matrix4x2dv', 'Matrix3x4dv', 'Matrix4x3dv',
]

def test_extensions(gldir, command):
  # See if removing an extension gives us a real entry
  for extension in extensions:
    if command[-len(extension):] == extension:
      command_file = shared.find_command_file(gldir, command[0:-len(extension)])
      if not command_file == False:
        return command[0:-len(extension)]
        
  return ""

def test_replacements(gldir, command):
  command_docs = test_extensions(gldir, command)

  if (len(command_docs)):
    return command_docs
  
  # Some commands need just a single letter removed
  command_test = command.replace("I", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("L", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Getn", "Get")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  if command_test != command:
    test = test_extensions(gldir, command_test)
    if len(test):
      return test

  command_test = command.replace("Readn", "Read")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  # Named commands are stored under their non-named equivalents
  command_test = command.replace("NamedFramebuffer", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("NamedFramebuffer", "Buffer")
  if command_test != command:
    test = test_extensions(gldir, command_test)
    if len(test):
      return test

  command_test = command.replace("Named", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  if command_test != command:
    test = test_extensions(gldir, command_test)
    if len(test):
      return test

  command_test = command.replace("Named", "").replace("Data", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Named", "").replace("SubData", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Texture", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("ArrayAttrib", "AttribArray")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("VertexArray", "Bind")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("Array", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("ArrayAttribI", "Attrib")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  command_test = command.replace("ArrayAttribL", "Attrib")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  # For glTextureBuffer -> glTexBuffer and glTextureBufferRange -> glTexBufferRange
  command_test = command.replace("ture", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  if command_test != command:
    return test_extensions(gldir, command_test)
    
  command_test = command.replace("ByRegion", "")
  if not shared.find_command_file(gldir, command_test) == False:
    return command_test

  return command

gltree = ET.parse('specs/gl.xml')
glroot = gltree.getroot()

output = open("opengl_spec.py", "w")
output.write("version_commands = {\n")

current_command_list = []
last_api = ""
for feature in glroot:
  if feature.tag != 'feature':
    continue

  if feature.attrib['api'] == 'gl' or feature.attrib['api'][0:4] == 'gles':
    gles = feature.attrib['api'][0:4] == 'gles'
    
    gl_prefix = 'gl'
    if gles:
      gl_prefix = 'es'
      
    if last_api != feature.attrib['api']:
      current_command_list = []
      last_api = feature.attrib['api']

    gl_major_version = feature.attrib['number'][0]
    for child in feature:
      if child.tag == 'require':
        if 'profile' in child.attrib and child.attrib['profile'] == 'compatibility':
          continue
        for command in child:
          if command.tag != 'command':
            continue
          current_command_list.append(command.attrib['name'])
      elif child.tag == 'remove':
        for command in child:
          if command.tag != 'command':
            continue
          current_command_list.remove(command.attrib['name'])

    output.write("  '" + gl_prefix + feature.attrib['number'] + "': {\n")
    for command in current_command_list:
      gldir = gl_prefix + gl_major_version
      
      command_docs = command
      
      # See if the reference file exists on disk
      if os.path.exists(gldir):
        command_file = shared.find_command_file(gldir, command)
        if command_file == False:
          command_docs = test_replacements(gldir, command)

          command_file = shared.find_command_file(gldir, command_docs)
        if command_file == False:
          print("No command docs file found for " + command + " (" + gl_prefix + gl_major_version + ")")
          output.close()
          assert(false)
        
      output.write("    '" + command + "': '" + command_docs + "',\n")
    output.write("  },\n")
    
output.write("}\n")
output.close()