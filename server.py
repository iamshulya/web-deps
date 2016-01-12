#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import os
import json
import subprocess

# Директория с deps2.0 для сервисов
services_dir_env = 'services/'
ROOT = '/vagrant/web-deps/'
SERVICE_DIR_ENV_ABS = ROOT + services_dir_env


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


@web_deps.route("/list_r") #Отображает список версий релизов из подпапки releases. Требует параметр service_dir.
def list_r():
    service_dir = flask.request.args.to_dict()['service_dir']
    return json.dumps(list_services(services_dir_env + service_dir + '/releases/'))

@web_deps.route("/list_serverstodeploy") #Отображает список серверов куда можно выложить данный релиз. Список серверов указывается в файле .serverstodeploy
def list_r1():
    service_dir = flask.request.args.to_dict()['service_dir']
    file = open(SERVICE_DIR_ENV_ABS + service_dir + '/.serverstodeploy', 'r')
    ln = file.readlines()
    file.close()
    ln = map(lambda s: s.strip(), ln)
    #dict([ln])
    return json.dumps(ln)
    #return json.dumps(list_services(services_dir_env + service_dir + '/releases/'))


@web_deps.route("/web_do")
def web_do():
    service_dir = flask.request.args.to_dict()['service_dir']
    release_dir = flask.request.args.to_dict()['release_dir']
    servers_to_deploy = flask.request.args.to_dict()['servers_to_deploy']
    #return json.dumps('cd ' + SERVICE_DIR_ENV_ABS + service_dir + ' && fab web-do:release=' + release_dir)
    cmd = 'cd ' + SERVICE_DIR_ENV_ABS + service_dir + ' && fab web-do:release=' + release_dir + ' -H ' + servers_to_deploy
    #return cmd
    a=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout,stderror=a.communicate()
    return cmd + '\n' + stdout + stderror

if __name__ == "__main__":
   web_deps.run(host='0.0.0.0')
