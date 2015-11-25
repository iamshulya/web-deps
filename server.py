#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import os
import json

# Директория с deps2.0 для сервисов
services_dir_env = 'services/'
ROOT = '/vagrant/web-deps'

web_deps = flask.Flask(__name__, static_folder=ROOT)

@web_deps.route('/')
@web_deps.route('/<path:path>')
def send_static(path = False):
    # Здесь мы посылаем всю статику клиенту - html, js скрипты, css стили
    print 'Requested file path: {0}'.format(path)

    if not path:
            return web_deps.send_static_file('index.html')

    return web_deps.send_static_file(path)



def list_services(services_dir):
    sorted_release_folder = [dirs for dirs in os.listdir(services_dir) if os.path.isdir(os.path.join(services_dir, dirs))] # Отображает только директории
    sorted_release_folder.sort()
    return sorted_release_folder


@web_deps.route("/ping")
def ping():
   return "pong"

@web_deps.route("/list_s") # Отображает список директорий в services_dir_env
def list_s():
    return json.dumps(list_services(services_dir_env))


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
