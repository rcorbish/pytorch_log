#!/bin/sh

export FLASK_APP=log_viewer
export FLASK_ENV=development
export APP_SETTINGS=config.DevelopmentConfig

if [ "${1}" = "--init" ]
then
    flask init-db
    shift
fi


flask run --port=8111 --host=0.0.0.0

