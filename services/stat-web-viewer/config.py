# -*- coding: utf-8 -*-
from fabric.api import *

preCommand = '/etc/init.d/jetty stop'
postCommand = '/etc/init.d/jetty start'
service_root = '/service'
local_releases_root = 'releases'
service_name = 'stat-web-viewer'
remote_releases_root = '/var/local/releases'
env.user = 'deps'  # Пользователь
env.key_filename = './id_rsa'
