#!/usr/bin/python

# This utility was used to strip the header and footer from the 4.3 docs xhtml files.

import os
import re

def strip_html():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("html/"):
    f.extend(filenames)

  for filename in f:
    print "Processing " + filename

    fp = open ("html/" + filename)
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

    fp = open("html/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

def strip_html2():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("html2/"):
    f.extend(filenames)

  for filename in f:
    print "Processing " + filename

    fp = open ("html2/" + filename)
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

    fp = open("html2/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

def strip_html3():
  f = []
  for (dirpath, dirnames, filenames) in os.walk("html3/"):
    f.extend(filenames)

  for filename in f:
    print "Processing " + filename

    fp = open ("html3/" + filename)
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

    fp = open("html3/" + filename, "w")
    for line in content:
      fp.write("%s" % line)
    fp.close()

strip_html()
strip_html2()
strip_html3()

