
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_file
)
from werkzeug.exceptions import abort

from log_viewer.db import get_db
from . import log_viewer

bp = Blueprint( 'log_main', __name__ )

@bp.route('/')
def index():    
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 
    return render_template( 'home.html', models=lv.models() )


@bp.route('/run/<string:model_name>/<string:data_name>/', methods=['DELETE'] )
def deleteModel( model_name, data_name ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 
    model = lv.get_model( model_name, data_namel )
    model.delete()
    return "OK"


@bp.route('/run/<string:model_name>/<string:data_name>/', methods=['GET'] )
def model( model_name, data_name ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 

    model = lv.get_model( model_name, data_name )
    return render_template( 'model.html', model=model )



@bp.route('/run/<string:model_name>/<string:data_name>/<string:time>/', methods=['DELETE'] )
def deleteRun( model_name, data_name, time ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 
    run = lv.get_run( model_name, data_name, time )
    run.delete()
    return "OK"


@bp.route('/run/<string:model_name>/<string:data_name>/<string:time>/', methods=['GET'] )
def run( model_name, data_name, time ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 

    run = lv.get_run( model_name, data_name, time )
    return render_template( 'run.html', run=run, model_name=model_name, data_name=data_name )



@bp.route('/run/<string:model_name>/<string:data_name>/<string:time>/movie', methods=['GET'] )
def movie( model_name, data_name, time ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 

    run = lv.get_run( model_name, data_name, time )
    iob = run.get_movie()
    send_file( iob, "image/gif" )



@bp.route('/run/<string:model_name>/<string:data_name>/<string:time>/<string:epoch>/')
def epoch( model_name, data_name, time, epoch ):
    lv = log_viewer.LogViewer( current_app.config['BASE_DIR'] ) 
    run = lv.get_run( model_name, data_name, time )

    epoch = run.get_epoch( epoch )
    return render_template( 'epoch.html', run=run, epoch=epoch )

