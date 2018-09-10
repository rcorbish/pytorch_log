
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from log_viewer.db import get_db
from . import log_viewer

bp = Blueprint( 'log_main', __name__ )

@bp.route('/')
def index():    
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 

    models = list( lv.models() )
    #models = []
    return render_template( 'home.html', models=models )



@bp.route('/run/<string:model>/<string:data>/<string:time>/')
def run( model, data, time ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 

    run = lv.get_run( model, data, time )
    return render_template( 'run.html', run=run )



@bp.route('/run/<string:model>/<string:data>/<string:time>/<string:epoch>/')
def epoch( model, data, time, epoch ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 

    epoch = lv.get_epoch( model, data, time, epoch )
    return render_template( 'epoch.html', epoch=epoch )

