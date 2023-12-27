#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

<<<<<<< HEAD
env.hosts = ["18.234.106.42", "34.224.5.203"]
=======
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
>>>>>>> c35738818e9506e08d5e98f3575fd3b3d96f44d8


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
<<<<<<< HEAD
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]
=======
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
>>>>>>> c35738818e9506e08d5e98f3575fd3b3d96f44d8

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
