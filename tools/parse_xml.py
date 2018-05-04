# Recursively walk through a .xml file, writing out just the children's names with dashes. 
#
import sys
import xml.etree.ElementTree as ET

#print(len(sys.argv))
if (len(sys.argv) < 2):
  print("Usage: " + sys.argv[0] + " <xml-file>")
  sys.exit(0)
else:
  xml_file = sys.argv[1]

tree = ET.parse(xml_file)
root = tree.getroot()

prefix = ''
def print_children(parent):
  global prefix
  for child in parent:
    print(prefix,child.tag)
    prefix += '-'
    print_children(child)
  prefix = prefix[1:]

print_children(root)
