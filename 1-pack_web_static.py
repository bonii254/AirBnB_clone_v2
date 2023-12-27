#!/usr/bin/python3

from fabric.api import local
from datetime import datetime


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
