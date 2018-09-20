#!/bin/sh

export FLASK_APP=log_viewer
export FLASK_ENV=development
export APP_SETTINGS=config.DevelopmentConfig
export LANG=C.UTF-8

if [ "${1}" = "--init" ]
then
    flask init-db
    exit
fi

if [ "${1}" = "--clean" ]
then
    flask clean
    exit
fi



flask run --port=8111 --host=0.0.0.0

