from collections import OrderedDict

import opengl_spec

version_commands = {}
commands_version = {}
version_commands_flat = {}
commands_version_flat = {}

# Maps glColor2d to glColor
function_aliases = {}
# Maps glColor to glColor2d
aliased_functions = {}

example_functions = {}
tutorial_functions = {}

examples = {
  'vertexarray_draw': {
    'description': 'Render a vertex array (not loaded into OpenGL) using texture UV, color, and normal vertex attributes.',
    'commands': [ 'glDrawArrays' ],
  },
  'vertexarray_draw_indexed': {
    'description': 'Render an indexed vertex array (not loaded into OpenGL) using texture UV and normal vertex attributes.',
    'commands': [ 'glVertexAttribPointer', 'glDrawElements' ],
  },
  'vbo_load': {
    'description': 'Load a vertex buffer into OpenGL for later rendering.',
    'commands': [ 'glGenBuffers', 'glBindBuffer', 'glBufferData', 'glBufferSubData', 'glGetBufferParameteriv', 'glDeleteBuffers' ],
  },
  'vbo_load_index': {
    'description': 'Load an index buffer into OpenGL for later rendering.',
    'commands': [ 'glGenBuffers', 'glBindBuffer', 'glBufferData', 'glBufferSubData', 'glGetBufferParameteriv', 'glDeleteBuffers' ],
  },
  'vbo_draw_indexed': {
    'description': 'Render an indexed buffer object using texture UV and normal vertex attributes.',
    'commands': [ 'glBindBuffer', 'glEnableVertexAttribArray', 'glVertexAttribPointer', 'glDrawElements' ],
  },
  'shader_compile': {
    'description': 'Compile a program from a vertex shader and a fragment shader.',
    'commands': [ 'glCreateShader', 'glShaderSource', 'glCompileShader', 'glGetShaderiv', 'glGetShaderInfoLog', 'glCreateProgram', 'glBindAttribLocation', 'glAttachShader', 'glLinkProgram', 'glGetProgramiv' ],
  },
  'shader_setup': {
    'description': 'Retrieve uniform data after the shader has been compiled',
    'commands': [ 'glGetAttribLocation', 'glBindFragDataLocation', 'glGetProgramiv', 'glGetActiveUniform' ],
  },
  'fbo_create_texture': {
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'description': 'Create a framebuffer object with a texture-based color attachment and a texture-based depth attachment. Using texture-based attachments allows sampling of those textures in shaders.',
    'commands': [ 'glGenTextures', 'glBindTexture', 'glTexParameteri', 'glTexImage2D', 'glGenFramebuffers', 'glBindFramebuffer', 'glFramebufferTexture2D', 'glCheckFramebufferStatus' ],
  },
  'fbo_create_renderbuffer': {
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'description': 'Create a framebuffer object with a renderbuffer-based color attachment and a renderbuffer-based depth attachment.',
    'commands': [ 'glGenRenderbuffers', 'glBindRenderbuffer', 'glRenderbufferStorage', 'glGenFramebuffers', 'glFramebufferRenderbuffer' ],
  },
  'fbo_blit': {
    'versions': [ 'gl3', 'gl4', 'es3' ],
    'description': 'Copy the contents of one framebuffer object to another by blitting.',
    'commands': [ 'glBindFramebuffer', 'glBlitFramebuffer' ],
  },
  'texture_create': {
    'description': 'Create a texture object with linear mipmaps and edge clamping.',
    'commands': [ 'glGenTextures', 'glBindTexture', 'glTexParameteri', 'glTexImage2D', 'glGenerateMipmap' ],
  },
  'texture_read': {
    'description': 'Read the texture from GPU memory into a buffer.',
    'commands': [ 'glGetTexImage' ],
  },
}

tutorials = {
  'open.gl drawing': {
    'name': 'open.gl - The Graphics Pipeline',
    'link': 'https://open.gl/drawing',
    'commands': ['glBindBuffer', 'glShaderSource', 'glDeleteShader', 'glDetachShader', 'glUseProgram',
      'glVertexAttribPointer', 'glDrawArrays', 'glGetError', 'glUniform', 'glDrawElements',
      'glGenBuffers', 'glBufferData', 'glCreateShader', 'glCompileShader', 'glGetShader',
      'glGetShaderInfoLog', 'glAttachShader', 'glBindFragDataLocation', 'glLinkProgram',
      'glGetAttribLocation', 'glEnableVertexAttribArray', 'glGenVertexArrays', 'glBindVertexArray',
      'glGetUniformLocation', 'glVertexAttribPointer'],
  },
  'open.gl textures': {
    'name': 'open.gl - Textures Objects and Parameters',
    'link': 'https://open.gl/textures',
    'commands': ['glTexParameter', 'glTexImage2D', 'glBindTexture', 'glActiveTexture', 'glUniform',
      'glGenerateMipmap', 'glVertexAttribPointer', 'glEnableVertexAttribArray'],
  },
  'open.gl transformations': {
    'name': 'open.gl - Transformations',
    'link': 'https://open.gl/transformations',
    'commands': ['glUniform'],
  },
  'open.gl depthstencils': {
    'name': 'open.gl - Depth and Stencil Buffers',
    'link': 'https://open.gl/depthstencils',
    'commands': ['glDrawArrays', 'glEnable', 'glClear', 'glStencilFunc', 'glStencilOp', 'glStencilMask', 'glColorMask', 'glDepthMask', 'glGetUniformLocation'],
  },
  'open.gl framebuffers': {
    'name': 'open.gl - Framebuffers',
    'link': 'https://open.gl/framebuffers',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glCheckFramebufferStatus', 'glReadPixels', 'glViewport', 'glBindFragDataLocation',
      'glDeleteRenderbuffers', 'glBindTexture', 'glGenFramebuffers', 'glBindFramebuffer',
      'glDeleteFramebuffers', 'glGenTextures', 'glTexImage2D', 'glTexParameter',
      'glFramebufferTexture2D', 'glGenRenderbuffers', 'glBindRenderbuffer', 'glRenderbufferStorage',
      'glFramebufferRenderbuffer', 'glBindVertexArray', 'glEnable', 'glUseProgram', 'glActiveTexture',
      ],
  },
  'open.gl geometry': {
    'name': 'open.gl - Geometry Shaders',
    'link': 'https://open.gl/geometry',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glCheckFramebufferStatus', 'glReadPixels', 'glViewport', 'glBindFragDataLocation',
      'glDeleteRenderbuffers', 'glBindTexture', 'glDrawArrays', 'glCreateProgram', 'glAttachShader',
      'glLinkProgram', 'glUseProgram', 'glBindBuffer', 'glBufferData', 'glGenVertexArrays',
      'glBindVertexArray', 'glGetAttribLocation', 'glEnableVertexAttribArray', 'glVertexAttribPointer',
      'glClearColor', 'glClear', 'glDrawArrays'],
  },
  'open.gl feedback': {
    'name': 'open.gl - Transform Feedback',
    'link': 'https://open.gl/feedback',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glCreateShader', 'glShaderSource', 'glCompileShader', 'glCreateProgram',
      'glAttachShader', 'glLinkProgram', 'glTransformFeedbackVaryings', 'glUseProgram',
      'glGenVertexArrays', 'glBindVertexArray', 'glGenBuffers', 'glBindBuffer', 'glBufferData',
      'glGetAttribLocation', 'glEnableVertexAttribArray', 'glVertexAttribPointer', 'glGenBuffers',
      'glBindBuffer', 'glBufferData', 'glEnable', 'glBindBufferBase', 'glBeginTransformFeedback',
      'glDrawArrays', 'glFlush', 'glGetBufferSubData', 'glGenQueries', 'glBeginQuery',  
      'glGetQueryObject'],
  },
  'songho overview': {
    'name': 'Songho - OpenGL Overview',
    'link': 'https://www.songho.ca/opengl/gl_overview.html',
    'versions': [ 'gl2', 'gl3' ],
    'commands': ['glColor', 'glVertex', 'glPushAttrib', 'glEnable', 'glBegin', 'glFlush', 'glFinish'],
  },
  'songho pipeline': {
    'name': 'Songho - OpenGL Rendering Pipeline',
    'link': 'https://www.songho.ca/opengl/gl_pipeline.html',
    'versions': [ 'gl2', 'gl3' ],
    'commands': ['glRenderMode', 'glReadPixels', 'glCopyPixels', 'glGet', 'glIsEnabled'],
  },
  'songho transformations': {
    'name': 'Songho - OpenGL Transformation',
    'link': 'https://www.songho.ca/opengl/gl_transform.html',
    'versions': [ 'gl2', 'gl3' ],
    'commands': ['glRotate', 'glTranslate', 'glScale', 'glViewport', 'glDepthRange', 'glMatrixMode',
      'glOrtho', 'glFrustum', 'glPushMatrix', 'glLoadIdentity', 'glLoadMatrix', 'glLoadTransposeMatrix',
      'glMultMatrix', 'glMultTransposeMatrix'],
  },
  'songho matrices': {
    'name': 'Songho - OpenGL Matrix Class (C++)',
    'link': 'https://www.songho.ca/opengl/gl_matrix.html',
    'versions': [ 'gl2', 'gl3' ],
    'commands': ['glRotate', 'glTranslate', 'glScale', 'glMultMatrix', 'glFrustum',
      'glOrtho', 'glLoadIdentity'],
  },
  'songho vertex array': {
    'name': 'Songho - OpenGL Vertex Array',
    'link': 'https://www.songho.ca/opengl/gl_vertexarray.html',
    'versions': [ 'gl2', 'gl3' ],
    'commands': ['glBegin', 'glVertex', 'glDrawArrays', 'glDrawElements', 'glDrawRangeElements',
      'glEnableClientState', 'glVertexPointer', 'glNormalPointer', 'glColorPointer', 'glIndexPointer',
      'glTexCoordPointer', 'glEdgeFlagPointer', 'glPolygonMode'],
  },
  'songho display lists': {
    'name': 'Songho - OpenGL Display List',
    'link': 'https://www.songho.ca/opengl/gl_displaylist.html',
    'versions': [ 'gl2', 'gl3' ],
    'commands': ['glFlush', 'glFinish', 'glRenderMode', 'glEnableClientState', 'glVertexPointer',
      'glIsEnabled', 'glGet', 'glReadPixels', 'glFeedbackBuffer', 'glGenLists', 'glVertex',
      'glDeleteLists', 'glNewList', 'glEndList', 'glCallList', 'glCallLists', 'glBegin', 'glListBase',
      'glDrawElements'],
  },
  'songho vbo': {
    'name': 'Songho - OpenGL Vertex Buffer Object (VBO)',
    'link': 'https://www.songho.ca/opengl/gl_vbo.html',
    'versions': [ 'gl2', 'gl3' ],
    'commands': ['glVertexPointer', 'glNormalPointer', 'glTexCoordPointer', 'glGenBuffers',
      'glBindBuffer', 'glBufferData', 'glBufferSubData', 'glDeleteBuffers', 'glEnableClientState',
      'glDrawElements', 'glMapBuffer', 'glUnmapBuffer'],
  },
  'songho pbo': {
    'name': 'Songho - OpenGL Pixel Buffer Object (PBO)',
    'link': 'https://www.songho.ca/opengl/gl_pbo.html',
    'commands': ['glGenBuffers', 'glBindBuffer', 'glBufferData', 'glMapBuffer', 'glUnmapBuffer',
      'glBufferData', 'glBindTexture', 'glTexSubImage2D'],
  },
  'songho fbo': {
    'name': 'Songho - OpenGL Frame Buffer Object (FBO)',
    'link': 'https://www.songho.ca/opengl/gl_fbo.html',
    'commands': ['glFramebufferTexture2D', 'glFramebufferRenderbuffer', 'glGenFramebuffers',
      'glDeleteFramebuffers', 'glBindFramebuffer', 'glGenRenderbuffers', 'glDeleteRenderbuffers', 
      'glBindRenderbuffer', 'glRenderbufferStorage', 'glGetRenderbufferParameter', 
      'glCheckFramebufferStatus', 'glBlitFramebuffer', 'glTexParameter', 'glTexImage2D',
      'glGenerateMipmap'],
  },
  'opengl-tutorial.org vao': {
    'name': 'opengl-tutorial.org - Tutorial 2 : The first triangle',
    'link': 'https://www.opengl-tutorial.org/beginners-tutorials/tutorial-2-the-first-triangle/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glGenVertexArrays', 'glBindVertexArray', 'glGenBuffers',
      'glBindBuffer', 'glBufferData', 'glEnableVertexAttribArray', 'glVertexAttribPointer', 
      'glDrawArrays', 'glCreateShader', 'glShaderSource', 'glCompileShader', 'glGetShader',
      'glGetShaderInfoLog', 'glAttachShader', 'glLinkProgram', 'glDeleteShader', 'glUseProgram'],
  },
  'opengl-tutorial.org matrices': {
    'name': 'opengl-tutorial.org - Tutorial 3 : Matrices',
    'link': 'https://www.opengl-tutorial.org/beginners-tutorials/tutorial-3-matrices/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glUniform'],
  },
  'opengl-tutorial.org colored cube': {
    'name': 'opengl-tutorial.org - Tutorial 4 : A Colored Cube',
    'link': 'https://www.opengl-tutorial.org/beginners-tutorials/tutorial-4-a-colored-cube/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glDrawArrays', 'glGenBuffers', 'glBindBuffer', 'glBufferData',
      'glEnableVertexAttribArray', 'glVertexAttribPointer', 'glEnable', 'glDepthFunc', 'glClear'],
  },
  'opengl-tutorial.org textured cube': {
    'name': 'opengl-tutorial.org - Tutorial 5 : A Textured Cube',
    'link': 'https://www.opengl-tutorial.org/beginners-tutorials/tutorial-5-a-textured-cube/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glGenTextures', 'glBindTexture', 'glTexImage2D', 'glTexParameter',
      'glGenerateMipmap', 'glCompressedTexImage2D', 'glEnable', 'glDepthFunc', 'glClear'],
  },
  'opengl-tutorial.org model loading': {
    'name': 'opengl-tutorial.org - Tutorial 7 : Model loading',
    'link': 'https://www.opengl-tutorial.org/beginners-tutorials/tutorial-7-model-loading/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glBufferData'],
  },
  'opengl-tutorial.org basic shading': {
    'name': 'opengl-tutorial.org - Tutorial 8 : Basic shading',
    'link': 'https://www.opengl-tutorial.org/beginners-tutorials/tutorial-8-basic-shading/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glGenBuffers', 'glBindBuffer', 'glBufferData', 'glEnableVertexAttribArray',
      'glVertexAttribPointer'],
  },
  'opengl-tutorial.org transparency': {
    'name': 'opengl-tutorial.org - Tutorial 10 : Transparency',
    'link': 'https://www.opengl-tutorial.org/intermediate-tutorials/tutorial-10-transparency/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glEnable', 'glBlendFunc'],
  },
  'opengl-tutorial.org normal mapping': {
    'name': 'opengl-tutorial.org - Tutorial 13 : Normal Mapping',
    'link': 'https://www.opengl-tutorial.org/intermediate-tutorials/tutorial-13-normal-mapping/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glGenBuffers', 'glBindBuffer', 'glBufferData', 'glGetUniformLocation',
      'glUniform', 'glActiveTexture', 'glBindTexture', 'glEnableVertexAttribArray',
      'glVertexAttribPointer', 'glDrawElements'],
  },
  'opengl-tutorial.org rtt': {
    'name': 'opengl-tutorial.org - Tutorial 14 : Render To Texture',
    'link': 'https://www.opengl-tutorial.org/intermediate-tutorials/tutorial-14-render-to-texture/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glGenFramebuffers', 'glBindFramebuffer', 'glGenTextures', 'glBindTexture',
      'glTexImage2D', 'glTexParameter', 'glGenRenderbuffers', 'glBindRenderbuffer', 
      'glRenderbufferStorage', 'glFramebufferRenderbuffer', 'glFramebufferTexture', 'glDrawBuffers',
      'glCheckFramebufferStatus', 'glViewport', 'glGenVertexArrays', 'glBindVertexArray', 'glGenBuffers',
      'glBindBuffer', 'glBufferData', 'glGetUniformLocation', 'glTexImage2D', 'glTexImage2DMultisample'],
  },
  'opengl-tutorial.org shadow mapping': {
    'name': 'opengl-tutorial.org - Tutorial 16 : Shadow mapping',
    'link': 'https://www.opengl-tutorial.org/intermediate-tutorials/tutorial-16-shadow-mapping/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glGenFramebuffers', 'glBindFramebuffer', 'glGenTextures', 'glBindTexture',
      'glTexImage2D', 'glTexParameter', 'glFramebufferTexture', 'glDrawBuffer',
      'glCheckFramebufferStatus', 'glUniform'],
  },
  'opengl-tutorial.org particles': {
    'name': 'opengl-tutorial.org - Particles / Instancing',
    'link': 'https://www.opengl-tutorial.org/intermediate-tutorials/billboards-particles/particles-instancing/',
    'versions': [ 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glGenBuffers', 'glBindBuffer', 'glBufferData', 'glBufferSubData',
      'glEnableVertexAttribArray', 'glVertexAttribPointer', 'glDrawArraysInstanced', 
      'glVertexAttribDivisor'],
  },
  'sebastien-nvidia tex compression': {
    'name': 'S&eacute;bastien Domin&eacute; - Using Texture Compression in OpenGL',
    'link': 'https://www.oldunreal.com/editing/s3tc/ARB_texture_compression.pdf',
    'versions': [ 'gl2', 'gl3', 'gl4', 'es2', 'es3' ],
    'commands': ['glBindTexture', 'glCompressedTexImage2D', 'glGetTexLevelParameter',
      'glGetCompressedTexImage'],
  },
  'nehe ios triangle': {
    'name': 'nehe.gamedev.net - iOS Lesson 02 - First Triangle',
    'link': 'https://nehe.gamedev.net/tutorial/ios_lesson_02__first_triangle/50001/',
    'versions': [ 'es2', 'es3' ],
    'commands': ['glGenBuffers', 'glBindBuffer', 'glBufferData', 'glUseProgram',
      'glGetAttribLocation', 'glEnableVertexAttribArray', 'glVertexAttribPointer', 'glDrawArrays'],
  },
  'gerdelan hello triangle': {
    'name': 'Anton Gerdelan - "Hello Triangle" - OpenGL 4 Up and Running',
    'link': 'https://antongerdelan.net/opengl/hellotriangle.html',
    'versions': [ 'gl4' ],
    'commands': ['glEnable', 'glDepthFunc', 'glGenBuffers', 'glBindBuffer', 'glBufferData',
      'glGenVertexArrays', 'glBindVertexArray', 'glEnableVertexAttribArray', 'glVertexAttribPointer', 
      'glCreateShader', 'glShaderSource', 'glCompileShader', 'glCreateProgram', 'glAttachShader',
      'glLinkProgram', 'glClear', 'glUseProgram', 'glBindVertexArray', 'glDrawArrays'],
  },
  'gerdelan shaders': {
    'name': 'Anton Gerdelan - OpenGL 4 Shaders',
    'link': 'https://antongerdelan.net/opengl/shaders.html',
    'versions': [ 'gl4' ],
    'commands': ['glCreateShader', 'glShaderSource', 'glCompileShader', 'glGetShader',
      'glGetShaderInfoLog', 'glDeleteShader', 'glCreateProgram', 'glAttachShader', 'glLinkProgram', 
      'glValidateProgram', 'glGetProgram', 'glGetProgramInfoLog', 'glUseProgram', 'glGetActiveAttrib',
      'glGetAttribLocation', 'glGetUniformLocation', 'glGetActiveUniform', 'glUniform'],
  },
  'gerdelan vbo': {
    'name': 'Anton Gerdelan - Vertex Buffer Objects',
    'link': 'https://antongerdelan.net/opengl/vertexbuffers.html',
    'versions': [ 'gl4' ],
    'commands': ['glGenBuffers', 'glBindBuffer', 'glBufferData', 'glVertexAttribPointer',
      'glEnableVertexAttribArray', 'glCompileShader', 'glAttachShader', 'glBindAttribLocation', 
      'glLinkProgram', 'glClear', 'glUseProgram', 'glBindVertexArray', 'glDrawArrays', 'glEnable',
      'glCullFace', 'glFrontFace', 'glGetActiveUniform', 'glUniform'],
  },
  'gerdelan cubemaps': {
    'name': 'Anton Gerdelan - Cube Maps: Sky Boxes and Environment Mapping',
    'link': 'https://antongerdelan.net/opengl/cubemaps.html',
    'versions': [ 'gl4' ],
    'commands': ['glGenBuffers', 'glBindBuffer', 'glBufferData', 'glVertexAttribPointer',
      'glEnableVertexAttribArray', 'glGenVertexArrays', 'glBindVertexArray', 'glActiveTexture', 
      'glGenTextures', 'glTexParameteri', 'glBindTexture', 'glTexImage2D', 'glUseProgram', 
      'glUniform', 'glDepthMask', 'glDrawArrays'],
  },
  'mckesson tut5': {
    'name': 'Learning Modern 3D Graphics Programming - Chapter 5. Objects in Depth [Vertex Array Objects, Indexed Drawing]',
    'link': 'https://web.archive.org/web/20150225192608/http://www.arcsynthesis.org/gltut/Positioning/Tutorial%2005.html',
    'versions': [ 'gl3', 'gl4' ],
    'commands': ['glGenVertexArrays', 'glBindVertexArray', 'glDrawElements', 'glBindBuffer',
      'glEnableVertexAttribArray', 'glVertexAttribPointer'],
  },
}

def get_major_versions(all_versions):
  major_versions = []
  for v in all_versions:
    major_version = v[:3]
    if not major_version in major_versions:
      major_versions.append(major_version)
      
  return major_versions

def get_major_versions_available(command):
  global commands_version_flat

  versions_available = commands_version_flat[command]
  versions_available.sort()
    
  return get_major_versions(versions_available)

def reverse_version_index(command_list):
  reversed = {}
  
  for version in command_list:
    for command in command_list[version]:
      if not command in reversed:
        reversed[command] = []

      reversed[command].append(version)
      reversed[command].sort()

  return reversed

def generate_versions():
  print("Generating OpenGL version index...")
  global version_commands
  global commands_version
  global version_commands_flat
  global commands_version_flat
  global function_aliases
  global aliased_functions
  
  version_commands = opengl_spec.version_commands

  for version in version_commands:
    version_commands_flat[version] = []
    
    for command in version_commands[version]:
      if int(version[2]) >= 2:
        if not command in function_aliases:
          function_aliases[command] = version_commands[version][command]

        if not version_commands[version][command] in aliased_functions:
          aliased_functions[version_commands[version][command]] = []
          
        if not command in aliased_functions[version_commands[version][command]]:
          aliased_functions[version_commands[version][command]].append(command)

        if not command in version_commands_flat[version]:
          version_commands_flat[version].append(version_commands[version][command])
  
  commands_version = reverse_version_index(version_commands)
  commands_version_flat = reverse_version_index(version_commands_flat)
  
  for example in examples:
    fp = open('html/examples/' + example + ".htm")
    examples[example]['code'] = fp.read()
    fp.close()
    
    for command in examples[example]['commands']:
      aliased_command = ""
      if command in function_aliases:
        aliased_command = function_aliases[command]
        
      assert aliased_command in commands_version_flat or command in commands_version_flat # This command was typed in wrong.

      if not command in example_functions:
        example_functions[command] = []
      example_functions_entry = {'example': example}
      if 'versions' in examples[example]:
        example_functions_entry['versions'] = examples[example]['versions']
      else:
        example_functions_entry['versions'] = get_major_versions(version_commands.keys())
      example_functions[command].append(example_functions_entry)

      if aliased_command != "" and aliased_command != command:
        if not aliased_command in example_functions:
          example_functions[aliased_command] = []
        example_functions_entry = {'example': example}
        if 'versions' in examples[example]:
          example_functions_entry['versions'] = examples[example]['versions']
        else:
          example_functions_entry['versions'] = get_major_versions(version_commands.keys())
        example_functions[aliased_command].append(example_functions_entry)

  for tutorial in tutorials:
    for command in tutorials[tutorial]['commands']:
      aliased_command = ""
      if command in function_aliases:
        aliased_command = function_aliases[command]

      assert aliased_command in commands_version_flat or command in commands_version_flat # This command was typed in wrong.

      if not command in tutorial_functions:
        tutorial_functions[command] = []
      tutorial_functions_entry = {'tutorial': tutorial}
      if 'versions' in tutorials[tutorial]:
        tutorial_functions_entry['versions'] = tutorials[tutorial]['versions']
      else:
        tutorial_functions_entry['versions'] = get_major_versions(version_commands.keys())
      tutorial_functions[command].append(tutorial_functions_entry)
        
      if aliased_command != "" and aliased_command != command:
        if not aliased_command in tutorial_functions:
          tutorial_functions[aliased_command] = []
        tutorial_functions_entry = {'tutorial': tutorial}
        if 'versions' in tutorials[tutorial]:
          tutorial_functions_entry['versions'] = tutorials[tutorial]['versions']
        else:
          tutorial_functions_entry['versions'] = get_major_versions(version_commands.keys())
        tutorial_functions[aliased_command].append(tutorial_functions_entry)

  print("Done.")

command_categories = OrderedDict([
  ( "Textures", [
    "glBindTexture", "glTexImage1D", "glTexImage2D", "glTexImage2DMultisample", "glTexImage3D",
    "glTexImage3DMultisample", "glTexParameter", "glCopyTexImage1D", "glCopyTexImage2D",
    "glCopyTexSubImage1D", "glCopyTexSubImage2D", "glCopyTexSubImage3D", "glGetTexParameter",
    "glGetTexImage", "glGetTexLevelParameter", "glDeleteTextures", "glGenTextures", "glIsTexture",
    "glTexSubImage1D", "glTexSubImage2D", "glTexSubImage3D", "glActiveTexture", "glCompressedTexImage1D",
    "glCompressedTexImage2D", "glCompressedTexImage3D", "glCompressedTexSubImage1D",
    "glCompressedTexSubImage2D", "glCompressedTexSubImage3D", "glGetCompressedTexImage", 
    "glBindImageTexture", "glBindImageTextures", "glBindTextureUnit", "glBindTextures", "glCreateTextures",
    "glGetCompressedTextureSubImage", "glGetTextureSubImage", "glTextureView", "glClearTexImage",
    "glClearTexSubImage", "glCopyImageSubData", "glTexStorage1D", "glTexStorage2D", "glTexStorage3D", 
    "glTexStorage2DMultisample", "glTexStorage3DMultisample", "glTexBuffer", "glTexBufferRange",
    "glInvalidateTexImage", "glInvalidateTexSubImage",
  ] ),
  ( "Rendering", [
    "glReadPixels", "glReadBuffer", "glDrawBuffer", "glClearDepth", "glClearDepthf", "glClearColor",
    "glClear", "glClearStencil", "glFinish", "glFlush", "glClearBuffer",
  ] ),
  ( "Frame Buffers", [
    "glIsRenderbuffer", "glBindRenderbuffer", "glDeleteRenderbuffers", "glGenRenderbuffers",
    "glRenderbufferStorage", "glGetRenderbufferParameter", "glGetRenderbufferParameteriv",
    "glIsFramebuffer", "glBindFramebuffer", "glDeleteFramebuffers", "glGenFramebuffers",
    "glCheckFramebufferStatus", "glFramebufferTexture", "glFramebufferRenderbuffer",
    "glGetFramebufferAttachmentParameter", "glGenerateMipmap", "glRenderbufferStorageMultisample",
    "glBlitFramebuffer", "glFramebufferTextureLayer", "glCreateFramebuffers", "glCreateRenderbuffers",
    "glDrawBuffers", "glFramebufferParameteri", "glGetFramebufferParameter",
    "glGetFramebufferParameteriv", "glInvalidateFramebuffer", "glInvalidateSubFramebuffer",
    "glSampleMaski", "glFramebufferTexture2D", "glGetFramebufferAttachmentParameteriv",
  ] ),
  ( "Shaders", [
    "glUniform", "glGetUniform", "glBindFragDataLocation", "glGetFragDataLocation",
    "glAttachShader", "glBindAttribLocation", "glCompileShader", "glCreateProgram", "glCreateShader",
    "glDeleteProgram", "glDeleteShader", "glDetachShader", "glGetActiveAttrib", "glGetActiveUniform",
    "glGetAttachedShaders", "glGetAttribLocation", "glGetProgram", "glGetProgramiv", "glGetProgramInfoLog",
    "glGetShader", "glGetShaderiv", "glGetShaderInfoLog", "glGetShaderSource", "glGetUniformLocation",
    "glIsProgram", "glIsShader", "glLinkProgram", "glShaderSource", "glUseProgram",
    "glValidateProgram", "glBindFragDataLocationIndexed", "glCreateShaderProgram",
    "glGetActiveAtomicCounterBufferiv", "glGetActiveSubroutineName", "glGetActiveSubroutineUniform",
    "glGetActiveSubroutineUniformName", "glGetActiveUniformBlock", "glGetActiveUniformBlockiv",
    "glGetActiveUniformBlockName", "glGetActiveUniformName", "glGetActiveUniformsiv",
    "glGetFragDataIndex", "glGetProgramBinary", "glProgramBinary", "glGetProgramResource",
    "glGetProgramResourceIndex", "glGetProgramResourceLocation", "glGetProgramResourceLocationIndex",
    "glGetProgramResourceName", "glGetProgramStage", "glGetShaderPrecisionFormat", "glGetSubroutineIndex",
    "glGetSubroutineUniformLocation", "glGetUniformBlockIndex", "glGetUniformIndices",
    "glGetUniformSubroutine", "glMinSampleShading", "glProgramParameter", "glProgramParameteri", 
    "glProgramUniform", "glReleaseShaderCompiler", "glShaderBinary", "glShaderStorageBlockBinding", 
    "glUniformBlockBinding", "glUniformSubroutines", "glUseProgramStages",
  ] ),
  ( "Buffer Objects", [
    "glBindBuffer", "glDeleteBuffers", "glGenBuffers", "glIsBuffer", "glBufferData", "glBufferSubData",
    "glGetBufferSubData", "glMapBuffer", "glUnmapBuffer", "glGetBufferParameter", "glGetBufferParameteriv",
    "glGetBufferPointerv", "glFlushMappedBufferRange", "glBindBufferRange", "glBindBufferBase",
    "glDrawArrays", "glDrawElements", "glDrawRangeElements", "glCreateBuffers",
    "glMultiDrawArrays", "glMultiDrawElements", "glEnableVertexAttribArray", "glDisableVertexAttribArray",
    "glGetVertexAttrib", "glGetVertexAttribPointerv", "glVertexAttrib", "glVertexAttribPointer",
    "glBindBuffersBase", "glBindBuffersRange", "glBindVertexBuffer", "glBindVertexBuffers", 
    "glBufferStorage", "glClearBufferData", "glClearBufferSubData", "glCopyBufferSubData", 
    "glCreateVertexArrays", "glVertexArrayElementBuffer", "glVertexAttribBinding", "glVertexAttribDivisor",
    "glVertexAttribFormat", "glVertexBindingDivisor", "glDrawArraysIndirect", "glDrawArraysInstanced",
    "glDrawArraysInstancedBaseInstance", "glDrawElementsBaseVertex", "glDrawElementsInstanced",
    "glDrawElementsInstancedBaseInstance", "glDrawRangeElementsBaseVertex", "glDrawElementsIndirect",
    "glDrawElementsInstancedBaseVertex", "glDrawElementsInstancedBaseVertexBaseInstance", 
    "glGetVertexArrayIndexed", "glGetVertexArrayiv", "glInvalidateBufferData", "glInvalidateBufferSubData",
    "glMapBufferRange", "glMultiDrawArraysIndirect", "glMultiDrawElementsBaseVertex", 
    "glMultiDrawElementsIndirect", "glPatchParameter", "glPrimitiveRestartIndex", "glProvokingVertex",
  ] ),
  ( "State Management", [
    # Anything that affects the state machine
    "glEnable", "glDisable", "glLogicOp", "glStencilFunc", "glStencilMask", "glColorMask", "glDepthMask",
    "glDepthRange", "glDepthRangef", "glHint", "glFrontFace",  "glLineWidth", "glCullFace", 
    "glPolygonMode", "glScissor", "glPointSize",  "glBlendFunc", "glStencilOp", "glDepthFunc", 
    "glPixelStore", "glPixelStorei", "glGet", "glGetError", "glIsEnabled", "glViewport",
    "glPolygonOffset", "glSampleCoverage", "glBlendFuncSeparate", "glPointParameter", "glBlendColor", 
    "glBlendEquation", "glStencilOpSeparate", "glStencilFuncSeparate", "glStencilMaskSeparate", 
    "glClampColor", "glBlendEquationSeparate", "glClipControl", "glDepthRangeArray",
    "glDepthRangeIndexed", "glScissorArray", "glScissorIndexed", "glViewportArray", 
    "glViewportIndexed",
  ] ),
  ( "Transform Feedback", [
    "glBeginTransformFeedback", "glEndTransformFeedback", "glTransformFeedbackVaryings",
    "glGetTransformFeedbackVarying", "glGenTransformFeedbacks", "glDeleteTransformFeedbacks",
    "glIsTransformFeedback", "glPauseTransformFeedback", "glResumeTransformFeedback",
    "glBindTransformFeedback", "glCreateTransformFeedbacks", "glDrawTransformFeedback",
    "glDrawTransformFeedbackInstanced", "glDrawTransformFeedbackStream", 
    "glDrawTransformFeedbackStreamInstanced", "glGetTransformFeedback", "glTransformFeedbackBufferBase",
    "glTransformFeedbackBufferRange",
  ] ),
  ( "Utility", [
   "glGetGraphicsResetStatus", "glGetString", "glGetInternalformat", "glGetInternalformativ", 
   "glGetMultisample", "glGetMultisamplefv", "glDispatchCompute", "glDispatchComputeIndirect",
   "glMemoryBarrier",
  ] ),
  ( "Queries", [
    "glGetQueryiv", "glGenQueries", "glDeleteQueries", "glBeginQuery", "glEndQuery", "glGetQueryObject",
    "glGetQueryObjectuiv", "glIsQuery", "glBeginQueryIndexed", "glEndQueryIndexed", "glGetQueryIndexed",
    "glQueryCounter", "glCreateQueries", "glBeginConditionalRender", "glEndConditionalRender",
  ] ),
  ( "Syncing", [
    "glTextureBarrier", "glClientWaitSync", "glDeleteSync", "glFenceSync", "glGetSync", "glGetSynciv", 
    "glIsSync", "glWaitSync"
  ] ),
  ( "Vertex Array Objects", [
    "glBindVertexArray", "glDeleteVertexArrays", "glGenVertexArrays", "glIsVertexArray"
  ] ),
  ( "Samplers", [
    "glGenSamplers", "glDeleteSamplers", "glSamplerParameter", "glGetSamplerParameter", "glBindSampler",
    "glBindSamplers", "glCreateSamplers", "glIsSampler",
  ] ),
  ( "Program Pipelines", [
    "glActiveShaderProgram", "glBindProgramPipeline", "glCreateProgramPipelines", 
    "glDeleteProgramPipelines", "glGenProgramPipelines", "glGetProgramPipeline", 
    "glGetProgramPipelineInfoLog", "glIsProgramPipeline", "glValidateProgramPipeline"
  ] ),
  ( "Immediate Mode", [
    # Stuff you can call between glBegin and glEnd
    "glBegin", "glEnd", "glVertex", "glColor", "glTexCoord", "glFogCoord", "glIndex", "glMaterial",
    "glMultiTexCoord", "glNormal", "glSecondaryColor", "glArrayElement", "glEvalCoord", "glEvalMesh",
    "glEvalPoint"
  ] ),
  ( "GL2 Rasterization", [
    # Anything render related that doesn't exist anymore
    "glRenderMode", "glFeedbackBuffer", "glPushName", "glLoadName", "glPassThrough", "glSelectBuffer",
    "glInitNames", "glLineStipple", "glPolygonStipple", "glDrawPixels", "glCopyPixels", "glRasterPos",
    "glWindowPos", "glRect", "glBitmap", "glClipPlane", "glClearIndex", "glFog", "glGetClipPlane",
    "glGetMap", "glGetPixelMap", "glGetPolygonStipple","glMap1", "glMap2", "glMapGrid", "glPopName",
    "glPixelZoom",
  ] ),
  ( "Client Arrays", [
    "glVertexPointer", "glEnableClientState", "glDisableClientState", "glFogCoordPointer",
    "glIndexPointer", "glInterleavedArrays", "glNormalPointer", "glPopClientAttrib", "glPushClientAttrib",
    "glSecondaryColorPointer", "glColorPointer", "glTexCoordPointer",
  ] ),
  ( "Fixed Function", [
    # Stuff that got moved into shaders
    "glEdgeFlag", "glEdgeFlagPointer", "glAlphaFunc", "glLight", "glColorMaterial",
    "glLightModel", "glAccum", "glClearAccum", "glGetLight", "glGetMaterial", "glGetTexEnv",
    "glTexEnv", "glTexGen", "glGetTexGen", "glIndexMask", "glPushAttrib", "glPopAttrib", "glShadeModel"
  ] ),
  ( "Matrix State", [
    "glLoadMatrix", "glLoadIdentity", "glMatrixMode", "glMultMatrix", "glMultTransposeMatrix",
    "glPushMatrix", "glPopMatrix", "glLoadTransposeMatrix", "glFrustum", "glOrtho", "glRotate",
    "glScale", "glTranslate"
  ] ),
  ( "GL2 Textures", [
    "glAreTexturesResident", "glPrioritizeTextures", "glClientActiveTexture", "glPixelMap",
    "glPixelTransfer"
  ] ),
  ( "Call Lists", [
    "glCallList", "glCallLists", "glIsList", "glDeleteLists", "glGenLists", "glNewList", "glEndList",
    "glListBase"
  ] ),
  #( "GLX", [
  #  "glXChooseFBConfig", "glXChooseVisual", "glXCopyContext", "glXCreateContext", "glXCreateGLXPixmap",
  #  "glXCreateNewContext", "glXCreatePbuffer", "glXCreatePixmap", "glXCreateWindow", "glXDestroyContext",
  #  "glXDestroyGLXPixmap", "glXDestroyPbuffer", "glXDestroyPixmap", "glXDestroyWindow",
  #  "glXFreeContextEXT", "glXGetClientString", "glXGetConfig", "glXGetContextIDEXT",
  #  "glXGetCurrentContext", "glXGetCurrentDisplay", "glXGetCurrentDrawable", "glXGetCurrentReadDrawable",
  #  "glXGetFBConfigAttrib", "glXGetFBConfigs", "glXGetProcAddress", "glXGetSelectedEvent",
  #  "glXGetVisualFromFBConfig", "glXImportContextEXT", "glXIntro", "glXIsDirect", "glXMakeContextCurrent",
  #  "glXMakeCurrent", "glXQueryContextInfoEXT", "glXQueryContext", "glXQueryDrawable",
  #  "glXQueryExtensionsString", "glXQueryExtension", "glXQueryServerString", "glXQueryVersion",
  #  "glXSelectEvent", "glXSwapBuffers", "glXUseXFont", "glXWaitGL", "glXWaitX",
  #] ),
  #( "GLU", [
  #  "gluBeginCurve", "gluBeginPolygon", "gluBeginSurface", "gluBeginTrim", "gluBuild1DMipmapLevels",
  #  "gluBuild1DMipmaps", "gluBuild2DMipmapLevels", "gluBuild2DMipmaps", "gluBuild3DMipmapLevels",
  #  "gluBuild3DMipmaps", "gluCheckExtension", "gluCylinder", "gluDeleteNurbsRenderer", "gluDeleteQuadric",
  #  "gluDeleteTess", "gluDisk", "gluEndCurve", "gluEndPolygon", "gluEndSurface", "gluEndTrim",
  #  "gluErrorString", "gluGetNurbsProperty", "gluGetString", "gluGetTessProperty",
  #  "gluLoadSamplingMatrices", "gluLookAt", "gluNewNurbsRenderer", "gluNewQuadric", "gluNewTess",
  #  "gluNextContour", "gluNurbsCallbackDataEXT", "gluNurbsCallbackData", "gluNurbsCallback",
  #  "gluNurbsCurve", "gluNurbsProperty", "gluNurbsSurface", "gluOrtho2D", "gluPartialDisk",
  #  "gluPerspective", "gluPickMatrix", "gluProject", "gluPwlCurve", "gluQuadricCallback",
  #  "gluQuadricDrawStyle", "gluQuadricNormals", "gluQuadricOrientation", "gluQuadricTexture",
  #  "gluScaleImage", "gluSphere", "gluTessBeginContour", "gluTessBeginPolygon", "gluTessCallback",
  #  "gluTessEndContour", "gluTessEndPolygon", "gluTessNormal", "gluTessProperty", "gluTessVertex",
  #  "gluUnProject4", "gluUnProject",
  #] ),
  ( "Debug", [
    "glDebugMessageCallback", "glDebugMessageControl", "glDebugMessageInsert",
    "glGetDebugMessageLog", "glGetObjectLabel", "glGetObjectPtrLabel", "glGetPointerv",  
    "glGetProgramInterface", "glObjectLabel", "glObjectPtrLabel", "glPopDebugGroup", "glPushDebugGroup"
  ] ),
])

generate_versions()
