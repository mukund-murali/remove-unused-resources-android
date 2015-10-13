#!/usr/bin/python
import os
import sys

from xml.dom.minidom import parse
import xml.dom.minidom


"""
XML structure for unused files.

?xml version="1.0" encoding="UTF-8"?>
<problems>
  <problem>
    <file>file://$PROJECT_DIR$/HealthifyMe/res/raw/license_mit.txt</file>
    <line>1</line>
    <module>HealthifyMe</module>
    <entry_point TYPE="file" FQNAME="file://$PROJECT_DIR$/HealthifyMe/res/raw/license_mit.txt" />
    <problem_class severity="WARNING" attribute_key="WARNING_ATTRIBUTES">Unused resources</problem_class>
    <hints />
    <description>&lt;html&gt;The resource &lt;code&gt;R.raw.license_mit&lt;/code&gt; appears to be unused&lt;/html&gt;</description>
  </problem>
</problems>
"""

PROJECT_DIR_STRING = "$PROJECT_DIR$"
project_dir_replacement = "/Users/mukundvis/HealthifyMe/phoenix"
source_filename = "/Users/mukundvis/HealthifyMe/phoenix/HealthifyMe/build/outputs/AndroidLintUnusedResources.xml"

TO_REPLACE = [
   (PROJECT_DIR_STRING, project_dir_replacement),
   ("file://", "")
]
FILE_TYPES_AVAILABLE = [
   ('drawable', 'res/drawable'),
   ('menu', 'res/menu'),
   ('layout', 'res/layout')
]
files_in_filetypes = {}
for file_type, _ in FILE_TYPES_AVAILABLE:
   files_in_filetypes[file_type] = []

CHOICE_VIEW = 1
CHOICE_DELETE = 2

def get_file_type_to_view_or_delete(choice):
   choice_string = 'view' if choice == CHOICE_VIEW else 'delete'
   print 'What do you want to {}?'.format(choice_string)
   for i, (file_type, file_extension) in enumerate(FILE_TYPES_AVAILABLE):
      print i + 1, file_type
   choice = int(raw_input('Your choice? '))
   file_type_to_delete = FILE_TYPES_AVAILABLE[choice-1][0]
   return file_type_to_delete


def delete_file(file_name):
   try:
      print 'deleting', file_name
      os.remove(file_name)
   except Exception as e:
      print e.message


def display_or_delete_files(file_type, files_in_filetypes, choice):
   files_removed = 0
   file_names = files_in_filetypes[file_type]
   for file_name in file_names:
      if choice == CHOICE_DELETE:
         delete_file(file_name)
      else:
         print file_name
      files_removed += 1
   print 'Total files:', files_removed


# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse(source_filename)
collection = DOMTree.documentElement
problems = collection.getElementsByTagName("problem")

for i, problem in enumerate(problems):
   file_name = problem.getElementsByTagName('file')[0].childNodes[0].data
   for replace_string, replacement_string in TO_REPLACE:
      file_name = file_name.replace(replace_string, replacement_string)

   for file_type, extension in FILE_TYPES_AVAILABLE:
      if extension in file_name:
         files_in_filetypes[file_type].append(file_name)
choice = int(raw_input('What do you want to do? 1. View files 2. Delete files? '))

if choice > 2:
   print 'Choice unknown'
   sys.exit(0)

file_type = get_file_type_to_view_or_delete(choice)
if choice == CHOICE_DELETE:
   print 'This will delete all unused {}.'.format(file_type)
   choice = raw_input('Do you want to proceed? This is unreversible action. (Y/n)')
   choice_ch = choice.lower()
   if choice_ch == 'y':
      display_or_delete_files(file_type, files_in_filetypes, CHOICE_DELETE)
   elif choice_ch == 'n':
      print 'aborted'
   else:
      print 'Choice unknown'
else:
   # Choice should be View since there is no other choice possible
   display_or_delete_files(file_type, files_in_filetypes, CHOICE_VIEW)
