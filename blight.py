#!/usr/bin/env python

# Copyright (c) 2015 Sergey Skovorodnikov

# blight - a CLI python script to change brightness for Intel brightness controls
#  located at /sys/class/backlight/intel_backlight/brightness.
#  Script needs to be run as root or given NOPASSWD in visudo. If that's done
#  there is a security risk to running this script.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Requires: standard python 2.7; Linux
# Tested to work on Debian 8 stable
# 
# Tested scenario:
#  use xbindkeys to bind brightness keys to a command blight -u 1, 
#  which will increment the brightness by 406.
#  Use xbindkeys -k to find out the exact commands to put into .bindkeysrc

import sys, getopt

gl_bright_file = "/sys/class/backlight/intel_backlight/brightness"
gl_increment = 406
gl_max_brightness = 4296
gl_min_brightness = 0
CONST_UP = "up"
CONST_DOWN = "down"

# FUNCTION
# Changes brightess level by multiplying increment by the factor given in
# command argument
def change_brighness(direction, factor):
    with open(gl_bright_file, "r+") as f:
        value = f.read()
        curr_bright = value.replace("\n", "") # trim new line char
        new_bright = calc_brightness(direction, curr_bright, factor)
        f.seek(0)
        f.write(str(new_bright) + "\n")
        f.truncate()
        f.close()
    read_brightness_file()

# FUNCTION
# Only reads the contents of the brightness file
def read_brightness_file():
    fd = open(gl_bright_file, "r")
    print fd.read()
    fd.close()

# FUNCTION
# Calculates the value of new brightness and makes sure it does not exceed
# maximum allowed value by Intel backlight
def calc_brightness(direction, curr_bright, factor):
    if direction == CONST_UP:
        new_brightness = int(curr_bright) + int(factor)*gl_increment
        if new_brightness > gl_max_brightness:
            new_brightness = gl_max_brightness
        print ("current brightness %s; increasing brightness by factor of %s" % (curr_bright, factor))
    elif direction == CONST_DOWN:
        new_brightness = int(curr_bright) - int(factor)*gl_increment
        if new_brightness < gl_min_brightness:
            new_brightness = gl_min_brightness
        print ("current brightness %s; decreasing brightness by factor of %s" % (curr_bright, factor))
    else:
        print("calc_brightness: ERROR. Invalid direction argument %s" % direction)
        new_brightness = curr_bright
    return new_brightness

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hu:d:")
    except getopt.GetoptError:
        print("Usage: -u to increase brightness; -d to reduce brightness")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: -u to increase brightness; -d to reduce brightness")
        elif opt in ("-u"):
            change_brighness(CONST_UP, arg)
        elif opt in ("-d"):
            change_brighness(CONST_DOWN, arg)
    
# Execute program
if __name__ == "__main__":
    main(sys.argv[1:])
