#!/usr/bin/python

# This utility was used to strip the header and footer from the 4.3 docs xhtml files.

import os
import re

def strip_gl2():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("gl2/"):
    f.extend(filenames)

  for filename in f:
    print("Processing " + filename)

    fp = open ("gl2/" + filename)
    content = fp.readlines()
    fp.close()

    # First two lines are junk.
    while not "xml-stylesheet" in content[0]:
      content.pop(0)

    m = re.search("body>(.*)", content[0])
    firstline = m.group(1)
    content.pop(0)
    content.insert(0, firstline + "\n")

    # The last line is junk
    content.pop()
    content.append("        </p></div></div>")

    fp = open("gl2/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

def strip_gl3():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("gl3/"):
    f.extend(filenames)

  for filename in f:
    print("Processing " + filename)

    fp = open ("gl3/" + filename)
    content = fp.readlines()
    fp.close()

    # First two lines are junk.
    while not "xml-stylesheet" in content[0]:
      content.pop(0)

    m = re.search("body>(.*)", content[0])
    firstline = m.group(1)
    content.pop(0)
    content.insert(0, firstline + "\n")

    # The last line is junk
    content.pop()
    content.append("        </p></div></div>")

    fp = open("gl3/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

def strip_gl4():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("gl4/"):
    f.extend(filenames)

  for filename in f:
    print("Processing " + filename)

    fp = open ("gl4/" + filename)
    content = fp.readlines()
    fp.close()

    while not "header" in content[0]:
      content.pop(0)

    # One more time to pop the header
    content.pop(0)

    # The last three lines are <footer /> </body> </html>
    content.pop()
    content.pop()
    content.pop()

    fp = open("gl4/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

strip_gl2()
strip_gl3()
strip_gl4()

def strip_es1():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("es1/"):
    f.extend(filenames)

  for filename in f:
    print("Processing " + filename)

    fp = open ("es1/" + filename)
    content = fp.readlines()
    fp.close()

    # First two lines are junk.
    while not "xml-stylesheet" in content[0]:
      content.pop(0)

    m = re.search("body>(.*)", content[0])
    firstline = m.group(1)
    content.pop(0)
    content.insert(0, firstline + "\n")

    # The last line is junk
    content.pop()
    content.append("        </p></div></div>")
    
    if filename[-4:] == ".xml":
      filename = filename[:-4] + ".xhtml"

    fp = open("es1/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

def strip_es2():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("es2/"):
    f.extend(filenames)

  for filename in f:
    print("Processing " + filename)

    fp = open ("es2/" + filename)
    content = fp.readlines()
    fp.close()

    # First two lines are junk.
    while not "xml-stylesheet" in content[0]:
      content.pop(0)

    m = re.search("body>(.*)", content[0])
    firstline = m.group(1)
    content.pop(0)
    content.insert(0, firstline + "\n")

    # The last line is junk
    content.pop()
    content.append("        </p></div></div>")
    
    if filename[-4:] == ".xml":
      filename = filename[:-4] + ".xhtml"

    fp = open("es2/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

def strip_es3():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("es3/"):
    f.extend(filenames)

  for filename in f:
    print("Processing " + filename)

    fp = open ("es3/" + filename)
    content = fp.readlines()
    fp.close()

    while not "header" in content[0]:
      content.pop(0)

    # One more time to pop the header
    content.pop(0)

    # The last three lines are <footer /> </body> </html>
    content.pop()
    content.pop()
    content.pop()

    fp = open("es3/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

strip_es1()
strip_es2()
strip_es3()