import os
import errno
import collections

import io
import re
import sys
import getopt
from dateutil import parser

def rmtree( root ) :
	for top,dirs,files in os.walk( root, topdown=False ) :
		for file in files :
        		fn = os.path.join( top, file )
        		print( "F:", fn )
		for dir in dirs :
        		fn = os.path.join( top, dir )
        		print( "D:", fn )

rmtree( "." )

