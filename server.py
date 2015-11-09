#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import os
import json

# Директория с deps2.0 для сервисов
services_dir_env = 'services/'

web_deps = flask.Flask(__name__)

def list_services(services_dir):
    sorted_release_folder = [dirs for dirs in os.listdir(services_dir) if os.path.isdir(os.path.join(services_dir, dirs))] # Отображает только директории
    sorted_release_folder.sort()
    return sorted_release_folder

@web_deps.route("/ping")
def ping():
   return "pong"

@web_deps.route("/list_s") # Отображает список директорий в services_dir_env
def list_s():
    return str(list_services(services_dir_env))


@web_deps.route("/list_r")
def list_r():
    service_dir = flask.request.args.to_dict()['service_dir']
    return str(list_services(services_dir_env + service_dir + '/releases/'))
#ping()

@web_deps.route("/add")
def add():
    user_id = flask.request.args.to_dict()['user_id']
    print flask.request.args.to_dict()
    return str(flask.request.args)


if __name__ == "__main__":
   web_deps.run(host='0.0.0.0')
