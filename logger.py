
import torch
import torch.nn as nn
import torchvision.utils as vutils

import os
import errno
import datetime
import collections


class Logger :

    def __init__(self, model_name, data_name, models=[] ):
        self.print_interval = 200
        now = datetime.datetime.now()
        dt = now.strftime('%Y-%m-%d %H:%M:%S') 
        self.data_subdir = '/var/tmp/runs/{}/{}/{}'.format(model_name, data_name, dt)
        self.makedir( self.data_subdir ) 

        with  open( self.data_subdir+"/models.txt", "w" ) as modelFile :
            for model in models :
                modelFile.write( repr( model ) )
                modelFile.write( "\n")
                modelFile.write( repr(model.optimizer) ) 
                modelFile.write( "\n\n")

        self.losses = []
        self.avg_losses = []
        self.logfile = open( self.data_subdir+"/logfile.txt", "a")

    def __enter__(self) :
        return self

    def __exit__(self, exc_type, exc_value, traceback ) :
        print( "Finished ... {}".format( exc_type ), file=self.logfile )

        if self.logfile :
            self.logfile.close()
        
    def makedir( self, dir ) :
        try:
            os.makedirs( dir )
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


    def get_epoch_dir( self, epoch ) :
        dn = ( self.data_subdir + "/epoch-{}" ).format( epoch )
        if not os.path.exists( dn ) :
            self.makedir( dn )
        return dn


    def log_images( self, X, epoch ) :
        X = X if isinstance( X, collections.Sequence ) else [ X ]
        image_num = 0 
        ed = self.get_epoch_dir( epoch )
        for img in X :
            fn = ( ed + "/image-{}.png" ).format( image_num )
            vutils.save_image( img.detach(), fn, nrow=4, normalize=True )
            image_num = image_num + 1


    def log( self, losses, epoch, n_batch, num_batches ) :
        a = [ x.item() if torch.is_tensor(x) else x for x in losses ]
        self.avg_losses.append( a )

        #print( self.avg_losses )
        if( (n_batch % self.print_interval ) == (self.print_interval-1)) :

            avgs = map( lambda x:sum(x)/len(x), zip(*self.avg_losses) )
            self.avg_losses = []            
            
            # print the current losses as a list - convert to string
            astr = " ".join( list( map( lambda e: ('%5.4f' % e), avgs ) )  )
            log_msg = "Epoch %4d    Batch [%5d/%5d ]  Losses %s" % ( epoch, n_batch+1, num_batches, astr  )
            self.log_msg( log_msg )
            print( log_msg )

            fn = self.data_subdir + '/losses'
            if os.path.exists( fn ) :
                os.rename( fn, fn+'.bak' )
            self.losses.append( a )
            torch.save( self.losses, fn )
                            
        
    def save_model( self, models, epoch ) :
        models = models if isinstance ( models, collections.Sequence ) else [ models ]

        model_num = 0
        for model in models :
            fn = ( self.data_subdir + "/model-{}").format( model_num )
            if os.path.exists( fn ) :
                os.rename( fn, fn+'.bak' )
            torch.save( model.state_dict(), fn )
            model_num = model_num + 1


    def log_msg( self, msg ) :
        now = datetime.datetime.now()
        print( ("{} " + msg ).format( now.strftime('%H:%M:%S.%f') ), file=self.logfile )
