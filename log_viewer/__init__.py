
import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__ )
    '''
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'log-viewer.sqlite' ),
    )
    '''
    app.config.from_pyfile( 'config.py', silent=False )
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    return app

