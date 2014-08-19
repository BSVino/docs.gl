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
  print "Generating version index..."
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
      
      if not aliased_command in example_functions:
        example_functions[aliased_command] = []
      example_functions_entry = {'example': example}
      if 'versions' in examples[example]:
        example_functions_entry['versions'] = examples[example]['versions']
      else:
        example_functions_entry['versions'] = get_major_versions(version_commands.keys())
      example_functions[aliased_command].append(example_functions_entry)

  print "Done."

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
    "glDepthRangeIndexed", "glDisablei", "glScissorArray", "glScissorIndexed", "glViewportArray", 
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
