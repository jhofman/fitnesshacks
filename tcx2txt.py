#!/usr/bin/env python
#
# file: tcx2txt.py
#
# description: converts garmin tcx files to delimited text files
#
# usage: see tcx2txt.py --help
#   tcx files are found on mac osx in
#     ~/Library/Application Support/Garmin/Devices/<deviceid>/History/
#
# requires: ElementTree, BeautifulSoup
#
# author: jake hofman (gmail: jhofman)
#

from xml.etree.ElementTree import fromstring
from time import strptime, strftime
from optparse import OptionParser
import sys
import re

# import tcx functions from tcx.py
from tcx import *

def parse_options():
    """
    parses input options using optparse
    """

    usage="""
    %prog [options]

    converts tcx file (given as argument or stdin) to delimited text file
    """

    parser=OptionParser(usage)

    parser.add_option("-i","--input",
                      dest="istream",
                      default=sys.stdin,
                      help="input tcx file (default: stdin)")
    parser.add_option("-o","--output",
                      dest="ostream",
                      default=sys.stdout,
                      help="output text file (default: stdout)")
    parser.add_option("-d","--delimiter",
                      dest="delimiter",
                      default="\t",
                      help="delimiter for output file (default: tab)")

    options, args = parser.parse_args()

    # open input file stream if given
    if isinstance(options.istream, str):
        options.istream = open(options.istream, 'r')

    # open output file stream if given
    if isinstance(options.ostream, str):
        options.ostream = open(options.ostream, 'w')

    return options.istream, options.ostream, options.delimiter


if __name__=='__main__':
    # get and parse options
    istream, ostream, delim = parse_options()

    # read xml contents
    xml = istream.read()

    # parse tcx file
    points = parsetcx(xml)

    # print results
    # (activity, lap, timestamp, seconds, lat, long, alt, dist, heart, cad)
    for point in points:
        ostream.write(delim.join(map(str, point))+'\n')
    
