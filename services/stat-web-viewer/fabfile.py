# -*- coding: utf-8 -*-
from config import *
import os
from menu import *
from fabric.api import *
from fabric.contrib.files import exists
from os.path import join

def mkdir_p(path):  # Создает директории на удаленной машине
    run('mkdir -p ' + path)


def mkdir_p_local(path):  # Создает директории на локальной машине
    local('mkdir -p ' + path)


def listdir(path):  # Выдает список файлов/директорий
    pathToFiles = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            pathToFiles.append(os.path.join(dirname, filename))
        if '.git' in dirnames:
            dirnames.remove('.git')
    return(pathToFiles)

def remEmptyDir(path): # Удаляет пустые директории
    for root, dirs, files in os.walk(path,topdown=False):
        for name in dirs:
            fname = join(root,name)
            if not os.listdir(fname): #to check wither the dir is empty
                #print fname
                os.removedirs(fname)
def f(s): # Тестовая функция для вывода в консоль.
    print s

@task()
def check_release_version(): # Проверка версии сервиса на удаленном сервере
    with warn_only():
	run('ls %s/%s > /tmp/.lastrelease' % (remote_releases_root, service_name))
    	run('if [ `find /tmp/.lastrelease -size 0`  ]; then `echo NO SUCH SERVICE > /tmp/.lastrelease`;fi')
    	get('/tmp/.lastrelease', '/tmp/.lastrelease')
    local('cat /tmp/.lastrelease >> ./.lastrelease')

@task(name='web-do')
def upload_to_server(release):
    """#### Example: fab upload_to_server:release=20150725T115311 ####"""
    run('mkdir -p %s/%s' % (remote_releases_root, service_name))
    put('releases/%s/' % release, '%s/%s' % (remote_releases_root, service_name), mode=0775)
    run('chown -R deps:adm %s/%s' % (remote_releases_root, service_name))
    sudo(preCommand, shell=False)
    run('find %s -type l | while read file; do if [[ `readlink $file` == *"%s"* ]]; then `unlink $file`; fi; done' % (service_root, service_name), shell=False)
    run('find %s/%s/%s -mindepth 1 -depth -type d -printf "%%P\\n" | while read dir; do mkdir -p %s/$dir; done' % (remote_releases_root, service_name, release, service_root), shell=False)
    run('find %s/%s/%s -type f -printf "%%P\\n" | while read file; do ln -sf /var/local/releases/%s/%s/$file %s/$file; done' % (remote_releases_root, service_name, release, service_name, release,  service_root))
    with cd('%s/%s' % (remote_releases_root, service_name)):
        run('rm -rf `ls -t | tail -n +2`')
    sudo(postCommand, shell=False)

@task(name='do')
def choose_release():
    """- Example: fab do -H server-hostname-or-ip-address"""
    remEmptyDir('releases')
    sorted_release_folder = os.listdir(local_releases_root)
    sorted_release_folder.sort()
    sorted_release_folder.reverse()
    m = Menu("########## Выбирите релиз ##########")
    for release_folder in sorted_release_folder:
        if os.path.isdir(os.path.join(local_releases_root,release_folder)):
            m.addoption(release_folder, lambda a=release_folder:upload_to_server(a))
    m.start()
