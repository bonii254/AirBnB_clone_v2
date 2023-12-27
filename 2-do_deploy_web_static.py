#!/usr/bin/python3
"""
Module creates .tgz archive, distributes it to the web servers"""

from fabric.api import local, run, put, env, cd
import os
from datetime import datetime

env.hosts = ['18.234.106.42', '34.224.5.203']


def do_pack():
    """a Fabric script that generates a .tgz archive from the
    contents of the web_static folder"""
    try:
        local("mkdir -p versions")
        current_time = datetime.now()
        archive_name = "web_static_{}.tgz".format(
            current_time.strftime("%Y%m%d%H%M%S"))
        result = local("tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception as e:
        print("Erro:", str(e))
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers,"""
    if not os.path.exists(archive_path):
        return false

    archive_name = os.path.basename(archive_path)
    archive_name_without_ext = os.path.splitext((path_name))[0]

    uploaded = put(archive_path, '/tmp/')
    if uploaded.failed:
        return false
    path = run('mkdir -p /data/web_static/releases/{}'.format(
        archive_name_without_ext))
    path = '/data/web_static/releases/{}'.format(archive_name_without_ext)
    if path.failed:
        return false

    uncompressed = run('tar -xzvf /temp/{}'.format(archive_name, path))
    if uncompressed.failed:
        return false

    run('rm -rf /tmp/{}'.format(archive_name))
    move = run("mv {}/web_static/* {}".format(path, path))
    if move.failed:
        return false

    with cd("/data/webstatic"):
        rm_lnk = run("rm -rf /data/web_static/current")
        if rm_lnk.failed:
            return false
        update_link = run("ln -sf {} /data/web_static/current".format(path))
        if update_lnk.failed:
            return False
    return True
