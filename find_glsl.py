# Move GLSL Docs from gl4 to sl4
# add GLSL Docs from es3 to el3
import shutil, glob, os ,ntpath
path = os.path.dirname(os.path.abspath(__file__))

filenames = glob.glob(path+"\\gl4\\"+'*.xhtml')

print path


if not os.path.exists("sl4"):
    os.makedirs("sl4")

for filename in filenames:
	#print filename
	with open(filename, 'r') as readfile:
		if(readfile.read().find("OpenGL Shading Language Version") != -1):
			readfile.close()
			print filename
			shutil.copy(filename, path+"\\sl4\\"+ ntpath.basename(filename))
			print "found :" + filename +" , moved to" + path +"/sl4" + ntpath.basename(filename)
			
if not os.path.exists("el3"):
    os.makedirs("el3")

filenames = glob.glob(path+"\\es3\\"+'*.xhtml')
	
for filename in filenames:
	#print filename
	with open(filename, 'r') as readfile:
		if(readfile.read().find("OpenGL ES Shading Language Version") != -1):
			readfile.close()
			print filename
			shutil.copy(filename, path+"\\el3\\"+ ntpath.basename(filename))
			print "found :" + filename +" , moved to" + path +"\\el3\\" + ntpath.basename(filename)