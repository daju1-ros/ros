#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

PKG = 'rosbagmigration'
import roslib; roslib.load_manifest(PKG)

import sys
import rosbagmigration

from optparse import OptionParser

import os

import re

def print_trans(old,new,indent):
  from_txt = "%s [%s]"%(old._type, old._md5sum)
  if new is not None:
    to_txt= "%s [%s]"%(new._type, new._md5sum)
  else:
    to_txt = "Unknown"
  print "    "*indent + " * From: %s"%(from_txt,)
  print "    "*indent + "   To:   %s"%(to_txt,)

if __name__ == '__main__':

  parser = OptionParser(usage="usage: makerule.py msg.saved [-a] output_rulefile [rulefile1, rulefile2, ...] [-n]")
  parser.add_option("-a","--append",action="store_true",dest="append",default=False)
  parser.add_option("-n","--noplugins",action="store_true",dest="noplugins",default=False)
  (options, args) = parser.parse_args()

  all_rules = []

  if len(args) >= 2:

    rulefile = args[1]

    if os.path.isfile(rulefile) and not options.append:
      print >> sys.stderr, "The file %s already exists.  Include -a if you intend to append."%rulefile
      exit(1)

    if not os.path.isfile(rulefile) and options.append:
      print >> sys.stderr, "The file %s does not exist, and so -a is invalid."%rulefile
      exit(1)

    if options.append:
      append_rule = [rulefile]
    else:
      append_rule = []


    f = open(sys.argv[1])

    if f is None:
      print >> sys.stderr, "Could not open message full definition: %s"
      sys.exit()

    type_line = f.readline()
    pat = re.compile(r"\[(.*)]:")
    type_match = pat.match(type_line)
    if type_match is None:
      print >> sys.stderr, "Full definition file malformed.  First line should be: '[my_package/my_msg]:'"
      sys.exit()

    old_type = type_match.groups()[0]
    old_full_text = f.read()
    f.close()

    old_class = roslib.genpy.generate_dynamic(old_type,old_full_text)[old_type]

    if old_class is None:
      print >> sys.stderr, "Could not generate class from full definition file."
      sys.exit()

    mm = rosbagmigration.MessageMigrator(args[2:]+append_rule,not options.noplugins)

    migrations = rosbagmigration.checkmessages(mm, [old_class])

    if migrations == []:
      print "Saved definition is up to date"
      exit(0)
    else:
      print "The following migrations need to occur:"
      for m in migrations:
        all_rules.extend(m[1])

        print_trans(m[0][0].old_class, m[0][-1].new_class, 0)
        if len(m[1]) > 0:
          print "    %d rules missing:"%(len(m[1]))
          for r in m[1]:
            print_trans(r.old_class, r.new_class,1)

    if rulefile is not None:

      output = ""
      rules_left = mm.filter_rules_unique(all_rules)

      if rules_left == []:
        print "\nNo additional rule files needed to be generated.  %s not created."%(rulefile)
        exit(0)

      while rules_left != []:
        extra_rules = []

        for r in rules_left:
          if r.new_class is None:
            print "The message type %s appears to have moved.  Please enter the type to migrate it to."%(r.old_class._type,)
            new_type = raw_input('>')
            new_class = roslib.message.get_message_class(new_type)
            while new_class is None:
              print "\'%s\' could not be found in your system.  Please make sure it is built."%new_type
              new_type = raw_input('>')
              new_class = roslib.message.get_message_class(new_type)
            new_rule = mm.make_update_rule(r.old_class, new_class)
            R = new_rule(mm, 'GENERATED.' + new_rule.__name__)
            R.find_sub_paths()
            new_rules = [r for r in mm.expand_rules(R.sub_rules) if r.valid == False]
            extra_rules.extend(new_rules)
            print 'Creating the migration rule for %s requires additional missing rules:'%new_type
            for nr in new_rules:
              print_trans(nr.old_class, nr.new_class,1)
            output += R.get_class_def()
          else:
            output += r.get_class_def()
        rules_left = mm.filter_rules_unique(extra_rules)
      f = open(rulefile, 'a')
      f.write(output)
      f.close()
      print "\nThe necessary rule files have been written to: %s"%(rulefile,)
    else:
        print "rulefile not specified"
  else:
    parser.error("Incorrect number of arguments")

