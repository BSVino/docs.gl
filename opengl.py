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
      if int(version[0]) >= 2:
        if not command in function_aliases:
          function_aliases[command] = version_commands[version][command]

        if not version_commands[version][command] in aliased_functions:
          aliased_functions[version_commands[version][command]] = []
          
        if not command in aliased_functions[version_commands[version][command]]:
          aliased_functions[version_commands[version][command]].append(command)

        if not function_aliases[command] in version_commands_flat[version]:
          version_commands_flat[version].append(function_aliases[command])
  
  commands_version = reverse_version_index(version_commands)
  commands_version_flat = reverse_version_index(version_commands_flat)
  print "Done."

command_categories = OrderedDict([
  ( "Textures", [
    "glBindTexture", "glTexImage1D", "glTexImage2D", "glTexImage2DMultisample", "glTexImage3D",
    "glTexImage3DMultisample", "glTexParameter", "glCopyTexImage1D", "glCopyTexImage2D",
    "glCopyTexSubImage1D", "glCopyTexSubImage2D", "glCopyTexSubImage3D", "glGetTexParameter"
  ] ),
  ( "Shaders", [
    "glVertexAttrib", "glGetVertexAttrib", "glVertexAttribPointer", "glUniform", "glGetUniform",
    "glBindFragDataLocation", "glGetFragDataLocation"
  ] ),
  ( "Rendering", [
    "glBeginConditionalRender", "glEndConditionalRender", "glReadPixels", "glReadBuffer", "glDrawBuffer",
    "glDepthRange", "glClearDepth", "glClearColor"
  ] ),
  ( "Frame Buffers", [
    "glIsRenderbuffer", "glBindRenderbuffer", "glDeleteRenderbuffers", "glGenRenderbuffers",
    "glRenderbufferStorage", "glGetRenderbufferParameter", "glIsFramebuffer", "glBindFramebuffer",
    "glDeleteFramebuffers", "glGenFramebuffers", "glCheckFramebufferStatus", "glFramebufferTexture",
    "glFramebufferRenderbuffer", "glGetFramebufferAttachmentParameter", "glGenerateMipmap",
    "glRenderbufferStorageMultisample", "glBlitFramebuffer", "glFramebufferTextureLayer"
  ] ),
  ( "Buffer Objects", [
    "glBindBuffer", "glDeleteBuffers", "glGenBuffers", "glIsBuffer", "glBufferData", "glBufferSubData",
    "glGetBufferSubData", "glMapBuffer", "glUnmapBuffer", "glGetBufferParameter", "glGetBufferParameteriv",
    "glGetBufferPointerv", "glFlushMappedBufferRange", "glBindBufferRange", "glBindBufferBase",
    "glBeginTransformFeedback", "glEndTransformFeedback", "glTransformFeedbackVaryings",
    "glGetTransformFeedbackVarying",
  ] ),
  ( "Vertex Array Objects", [
    "glBindVertexArray", "glDeleteVertexArrays", "glGenVertexArrays", "glIsVertexArray"
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
])

generate_versions()

def get_major_versions(all_versions):
  major_versions = []
  for v in all_versions:
    major_version = v[0]
    if not major_version in major_versions:
      major_versions.append(major_version)
      
  return major_versions

def get_major_versions_available(command):
  global commands_version_flat

  versions_available = commands_version_flat[command]
  versions_available.sort()
    
  return get_major_versions(versions_available)