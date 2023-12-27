#!/usr/bin/python3
"""Module creates .tgz archive, distributes it to the web servers"""
import os
from fabric.api import local, cd, put, run, env
from datetime import datetime

env.hosts = ['18.234.106.42', '34.224.5.203']


def do_pack():
    """Generates a .tgz archive form contents of web static."""
    try:
        local("mkdir -p versions")
        current_time = datetime.now()
        archive_filename = "web_static_{}.tgz".format(
            current_time.strftime("%Y%m%d%H%M%S"))
        local("tar -czvf versions/{} web_static".format(archive_filename))
        return "versions/{}".format(archive_filename)
    except Exception as e:
        print("Error:", str(e))
        return None


def do_deploy(archive_path):
    """Deploys static files to our web servers.

    Atributes:
        archive_path(str): path to archive with our static files.
    Returns:
        True(boolean): on success,
        False(boolean): on fail.
    """
    if not os.path.exists(archive_path):
        return False
    archive_name = os.path.basename(archive_path)
    archive_name_without_ext = os.path.splitext((archive_name))[0]
    uploaded = put(archive_path, "/tmp/")
    if uploaded.failed:
        return false

    path = run('mkdir -p /data/web_static/releases/{}'.format(
        archive_name_without_ext))
    if path.failed:
        return false

    path = '/data/web_static/releases/{}'.format(archive_name_without_ext)
    uncompressed = run("tar -xzvf /tmp/{} -C {}".format(archive_name, path))
    if uncompressed.failed:
        return false

    run('rm -rf /tmp/{}'.format(archive_name))
    move = run("mv {}/web_static/* {}".format(path, path))
    if move.failed:
        return false

    with cd("/data/web_static"):
        rm_lnk = run("rm -rf /data/web_static/current")
        if rm_lnk.failed:
            return False
        update_lnk = run("ln -sf  {} /data/web_static/current".format(path))
        if update_lnk.failed:
            return False
    return true
