
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

    return render_template( 'home.html', models=lv.models() )



@bp.route('/run/<string:model>/<string:data>/<string:time>/')
def run( model, data, time ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 

    run = lv.get_run( model, data, time )
    return render_template( 'run.html', run=run )



@bp.route('/run/<string:model>/<string:data>/<string:time>/', methods=['DELETE'] )
def delete( model, data, time ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 
    run = lv.get_run( model, data, time )
    run.delete()
    return "OK"


@bp.route('/run/<string:model>/<string:data>/<string:time>/<string:epoch>/')
def epoch( model, data, time, epoch ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 
    run = lv.get_run( model, data, time )

    epoch = run.get_epoch( epoch )
    return render_template( 'epoch.html', run=run, epoch=epoch )

