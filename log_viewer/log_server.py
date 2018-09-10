
import os
import errno
import datetime
import collections

import torch
import torch.nn as nn
import torchvision.utils as vutils

import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as transforms

import re
import sys
import getopt
from dateutil import parser
import imageio

from flask import Flask
app = Flask( __name__ )


from http.server import HTTPServer, BaseHTTPRequestHandler

import log_viewer

class LogServer(HTTPServer):
    def __init__( self, run_dir ) :
        super(LogServer, self).__init__( ('0.0.0.0',8111), LogServerHandler )
        self.run_dir = run_dir

    def start( self ) :
        self.serve_forever()



class LogServerHandler( BaseHTTPRequestHandler) :

    def do_GET( self ) :
        print( "Boo Ya", self.server )
        self.send_response( 200 )
        self.end_headers()

        lv = log_viewer.LogViewer( self.server.run_dir )
        for model in lv.models() :
            self.wfile.write( b"<br>" )
            s = model.model_name + ":" + model.data_name
            self.wfile.write( s.bytes() )

        



def main() :
    try:
        _, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except Exception as msg :
        print( msg )
        print( "for help use --help" )
        sys.exit(2)

    run_dir = 'runs' if len(args) == 0 else args[0]
    ls = LogServer( run_dir ) 
    ls.start() 

    lv = log_viewer.LogViewer( run_dir )
    for model in lv.models() :
        print( model.model_name + ":" + model.data_name )
        latest = model.most_recent()
        print( "Last run at {}".format( latest.time ) )
        logs = latest.get_logs()
        print( "".join( logs[-10:] ) )
        images = []
        for epoch in latest.epochs() :
            img = epoch.get_image()
            if img is not None :
                images.append( img )
        imageio.mimsave( latest.base_dir + "/images.gif", images, duration=0.25, loop=1  )

        l = latest.get_losses()
        if l is not None :
            plt.figure()
            plt.plot( l ) 
            plt.show()


if __name__ == "__main__":
    main()
