#! /usr/bin/python
""" An FTP automation utility

squirt.py

Copyright (C) 2012 - Paul Pritchard

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>. """

import sys
import argparse
from funlayer import *

def build_script(options):
    """ Build a reusable FTP script 
        options is the dictionary of options that define the script """
    script = dict(script=options.script)
    script.update(host=options.host)
    script.update(user=options.user)
    script.update(password=options.password)
    script.update(local=options.local)
    script.update(remote=options.remote)
    script.update(do=options.do)
    script.update(files=options.files)

    can_we_build_it = fn_build_script(script)
    if can_we_build_it == 'Fail':
        return "Build of script %s failed. Check your options" % script.get('script')
    else:
        return "Script %s successfully %s" % (script.get('script'), can_we_build_it)

def copy_script(settings):
    """ Copy an existing script 
        options is the dictionary of options that define the script """
    script = dict(cf=settings.cf)
    script.update(ct=settings.ct)
    script.update(host=settings.host)
    script.update(user=settings.user)
    script.update(password=settings.password)
    script.update(local=settings.local)
    script.update(remote=settings.remote)
    script.update(do=settings.do)
    script.update(files=settings.files)

    if fn_copy_script(script) == True:
        print "Script %s successfully copied to %s" % (script.get('cf'), script.get('ct'))
    else:
        print "Copy of script %s to %s failed. Check your settings" % (script.get('cf'), script.get('ct'))

def delete_script(options):
    """ Delete an existing script """
    if fn_delete_script(options.script) == True:
        print "Script %s deleted" % options.script
    else:
        print "Error: Script %s not deleted" % options.script

def display_script(options):
    """ Displays a script
        options is a dictionay that contains one value - the script name """
    script = fn_retrieve_script(options.script)
    if script.get('exists') == False:
        print "Script %s not defined" % script.get('script')
    else:
        print "Script:        %s " % script.get('script')
        print "Host:          %s " % script.get('host')
        print "User:          %s " % script.get('user')
        print "Password:      %s " % script.get('password')
        print "Local folder:  %s " % script.get('local')
        print "Remote folder: %s " % script.get('remote')
        print "Action:        %s " % script.get('do')
        print "Files:         %s " % script.get('files')

def list_scripts():
    """ Lists the currently defined set of scripts 
        No paramerters this time """
    for script in  fn_list_scripts():
        print script

def execute_script(options):
    """ Execute a built script
        options is the dictionary of optional overrides applied to the script """
    script = dict(script=options.script)
    script.update(host=options.host)
    script.update(user=options.user)
    script.update(password=options.password)
    script.update(local=options.local)
    script.update(remote=options.remote)
    script.update(do=options.do)
    script.update(files=options.files)

    print "Script %s..." % script.get('script')
    result = fn_execute_script(script)
    file_list = result.get('files')
    if file_list != None and file_list != []:
        print "Files found..."
        for filename in file_list:
            print "   " + filename
    else:
        print "No files found"
    if result.get('status') == True:
        print "completed normally" 
    else:
        print "Failed"

def initialise_db():
    """ Initialise the database
        Use with care because if anything already exists - it will be deleted """
    return fn_initialise()

def main():
    """ The main event 
        Parses the entered arguments and figures out what to do with them """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Commands')
    
    # The build command
    build_parser = subparsers.add_parser('build', help='Build script')
    build_parser.add_argument('script', action='store', help='Script name')
    build_parser.add_argument('--host', action='store', help='Host name')
    build_parser.add_argument('--user', action='store', help='User ID')
    build_parser.add_argument('--password', action='store', help='Password')
    build_parser.add_argument('--local', action='store', help='Set local path')
    build_parser.add_argument('--remote', action='store', help='Set remote path')
    build_parser.add_argument('--do', action='store', help='Do action')
    build_parser.add_argument('--files', action='store', help='The files to be acted on')
    build_parser.set_defaults(command='build')

    # The copy command
    copy_parser = subparsers.add_parser('copy', help='Copy script')
    copy_parser.add_argument('cf', action='store', help='Copy from script')
    copy_parser.add_argument('ct', action='store', help='Copy to script')
    copy_parser.add_argument('--host', action='store', help='Host name')
    copy_parser.add_argument('--user', action='store', help='User ID')
    copy_parser.add_argument('--password', action='store', help='Password')
    copy_parser.add_argument('--local', action='store', help='Set local path')
    copy_parser.add_argument('--remote', action='store', help='Set remote path')
    copy_parser.add_argument('--do', action='store', help='Do action')
    copy_parser.add_argument('--files', action='store', help='The files to be acted on')
    copy_parser.set_defaults(command='copy')

    # The delete command
    delete_parser = subparsers.add_parser('delete', help='Delete script')
    delete_parser.add_argument('script', action='store', help='Script name')
    delete_parser.set_defaults(command='delete')

    # The display command
    display_parser = subparsers.add_parser('display', help='Display script')
    display_parser.add_argument('script', action='store', help='Script name')
    display_parser.set_defaults(command='display')

    # The list command
    list_parser = subparsers.add_parser('list', help='List currently defined scripts')
    list_parser.set_defaults(command='list')

    # The exec command
    exec_parser = subparsers.add_parser('exec', help='Execute script')
    exec_parser.add_argument('script', action='store', help='Script name')
    exec_parser.add_argument('--host', action='store', help='Host name')
    exec_parser.add_argument('--user', action='store', help='User ID')
    exec_parser.add_argument('--password', action='store', help='Password')
    exec_parser.add_argument('--local', action='store', help='Set local path')
    exec_parser.add_argument('--remote', action='store', help='Set remote path')
    exec_parser.add_argument('--do', action='store', help='Do action')
    exec_parser.add_argument('--files', action='store', help='The files to be acted on')
    exec_parser.set_defaults(command='exec')

    # The init command
    init_parser = subparsers.add_parser('init', help='Initialise')
    init_parser.set_defaults(command='init')

    try:
        command_line = parser.parse_args()
    except:
        sys.exit(2)

    if command_line.command == 'build':
        print build_script(command_line)
    if command_line.command == 'copy':
        copy_script(command_line)
    elif command_line.command == 'delete':
        delete_script(command_line)
    elif command_line.command == 'display':
        display_script(command_line)
    elif command_line.command == 'list':
        list_scripts()
    elif command_line.command == 'exec':
        execute_script(command_line)
    elif command_line.command == 'init':
        print initialise_db()
    else:
        print "Oops"
        sys.exit(2)

if __name__ == "__main__":
    main()
