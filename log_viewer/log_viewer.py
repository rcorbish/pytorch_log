
import torch
import torch.nn as nn
import torchvision.utils as vutils

import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as transforms

import os
import errno
import datetime
import collections

import io
import re
import sys
import getopt
from dateutil import parser
import imageio
import base64
'''
    This contains the representations of a test run of a model,
    each epoch it ran and the model setup and parameters
'''
def rmtree( root ) :
    '''
    recursively delete the root directory

    @parameters
    root: the name of the root directory
    '''
    for top,dirs,files in os.walk( root, topdown=False ) :
        for file in files :
            fn = os.path.join( top, file )
            os.remove( fn )
        for dir in dirs :
            fn = os.path.join( top, dir )
            os.rmdir( fn )
    os.rmdir( top )



class LogViewer :
    '''
    The main class through which models, runs and epochs
    are accessed. It manages data under a (configured) 
    root directory.
    '''
    def __init__(self, base_dir ):
        self.base_dir = base_dir
        try:
            os.makedirs( self.base_dir )
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


    def models( self ) :
        model_names = os.listdir( self.base_dir )
        for model_name in model_names :
            model_dir = self.base_dir + r"/" + model_name
            data_names = os.listdir( model_dir )
            for data_name in data_names :
                model = self.get_model( model_name, data_name )
                yield model


    def get_model( self, model_name, data_name ) :
        bn = self.base_dir + r"/" + model_name + r"/" + data_name
        model = Model( model_name, data_name, bn )
        return model 


    def get_run( self, model_name, data_name, run_time ) :
        model = self.get_model( model_name, data_name )
        run = Run( model, run_time  )
        return run


    def get_epoch( self, model_name, data_name, run_time, epoch ) :
        model = self.get_model( model_name, data_name )
        run = Run( model, run_time  )
        epoch = run.get_epoch( epoch )
        return epoch

    def clean( self ) :
        for model in self.models() :
            model.clean()


class Model  :
    def __init__(self, model_name, data_name, base_dir ):
        self.model_name = model_name
        self.data_name = data_name
        self.base_dir = base_dir 

    def runs( self ) :
        rg = r'\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2}'
        r = [ x for x in os.listdir( self.base_dir ) if re.match( rg, x ) is not None ] 
        s = sorted( r, key=lambda x : datetime.datetime.strptime( x, r'%Y-%m-%d %H:%M:%S' ), reverse=True )
 
        for run_time in s :
            run = Run( self, run_time )
            yield run 


    def most_recent( self, n=0 ) :
        r = list( self.runs() ) 
        s = sorted( r, key=lambda x : x.time, reverse=True )
        return s[n] if n<len(s) else None


    def get_run( self, run_time ) :
        run = Run( self, run_time  )
        return run


    def delete_run( self, run_time ) :
        run = Run( self, run_time  )
        run.delete() 


    def delete( self ) :
        rmtree( self.base_dir )


    def clean( self ) :
        for run in self.runs() :
            run.clean()

        runs = list( self.runs() )
        if len(runs) == 0 :
            os.rmdir( self.base_dir )


class Run :
    def __init__(self, model, run_time ):
        self.time = parser.parse( run_time )
        self.base_dir = model.base_dir + "/" + run_time

    def epochs( self ) :
        epoch_names = [ x for x in os.listdir( self.base_dir ) if x.startswith(r'epoch-') ] 
        get_integers_from_string = lambda x :  int( ''.join( [ s for s in re.split( '\D+', x ) if s.isdigit() ] ) )
        epoch_names = sorted( epoch_names, key=get_integers_from_string, reverse=True )
        for epoch_name in epoch_names :
            epoch = Epoch( epoch_name, self.base_dir )
            yield epoch

    def get_epoch( self, epoch_name ) :
        epoch = Epoch( epoch_name, self.base_dir )
        return epoch

    def get_losses( self ) :
        fn = self.base_dir + r'/losses'
        L = torch.load( fn ) if os.path.exists( fn ) else []
        return L

    def get_base64_losses( self ) :
        L = self.get_losses()
        plt.figure()
        plt.plot( L ) 
        buf = io.BytesIO()
        plt.savefig( buf, format='png' )
        encoded = base64.b64encode( buf.getvalue() ).decode()
        return r'data:image/png;base64,{}'.format( encoded )


    def get_logs( self, tail=50 ) :
        lines = []
        try :
            with open( self.base_dir + r'/logfile.txt' ) as f :
                lines = f.readlines()
            return lines[-tail:]
        except Exception :
            return []


    def get_model_specs( self ) :
        lines = []
        try :
            with open( self.base_dir + r'/models.txt' ) as f :
                lines = f.readlines()
            return lines
        except Exception :
            return []
       

    def delete( self ) :
        rmtree( self.base_dir )


    def clean( self ) :
        for epoch in self.epochs() :
            epoch.clean()

        epochs = list( self.epochs() )
        if len(epochs) == 0 :
            os.rmdir( self.base_dir )



class Epoch : 
    def __init__(self, name, base_dir ):
        self.name = name
        self.base_dir = base_dir + r"/" + name


    def get_image_file( self, index=0 ) :
        fn = self.base_dir + r'/image-{}.png'.format( index )
        if os.path.exists( fn ) :
            return fn 
        if index == 0 :
            fn = self.base_dir + r'/image.png'
            if os.path.exists( fn ) :
                return fn
        return None      



    def get_image( self, index=0 ) :
        fn = self.get_image_file( index )
        if fn is not None :
            return imageio.imread( fn )
        return None



    def get_base64_image( self, index=0 ) :
        fn = self.get_image_file( index )
        if fn is not None :
            encoded = base64.b64encode(open( fn, "rb").read()).decode()
            return r'data:image/png;base64,{}'.format( encoded )
        return None



    def get_params( self ) :
        pass


    def delete( self ) :
        for file in os.listdir( self.base_dir ) :
            os.remove( file )


    def clean( self ) :
        files = list( os.listdir( self.base_dir ) )
        if len(files) == 0 :
            os.rmdir( self.base_dir )
