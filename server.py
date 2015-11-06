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

@web_deps.route("/list_s")
def list_s():
    return str(list_services(services_dir_env))


@web_deps.route("/list_r")
def list_r():
    return str(list_services(services_dir_env + list_services(services_dir_env)[0] + '/'))
#ping()



if __name__ == "__main__":
   web_deps.run(host='0.0.0.0')
