# Copy GLSL Docs from gl4 to sl4
# Copy GLSL Docs from es3 to el3

import shutil, glob, os ,ntpath
path = os.path.dirname(os.path.abspath(__file__))

def make_glsl_docs():

    print("Creating GLSL docs ...")
    sl_filenames = glob.glob(path+"\\gl4\\"+'*.xhtml')
    if not os.path.exists("sl4"):
        os.makedirs("sl4")
    get_glsl_docs(sl_filenames , "sl4")
    
    es_filenames = glob.glob(path+"\\es3\\"+'*.xhtml')
    if not os.path.exists("el3"):
        os.makedirs("el3")
    get_glsl_docs(es_filenames , "el3" )
    print("done")


def get_glsl_docs( filenames, foldername ):

    findtext = ""
    if foldername[0:2] == "el":
        findtext = "OpenGL ES Shading Language Version"
    elif foldername[0:2] == "sl":
        findtext = "OpenGL Shading Language Version"
        
    print(foldername[0:2])
    for filename in filenames:
        with open(filename, 'r') as readfile:
            if(readfile.read().find(findtext) != -1):
                readfile.close()
                #change .copy .move to get them out of GL directories
                shutil.copy(filename, path+"\\"+foldername+"\\"+ ntpath.basename(filename))
                
make_glsl_docs()                