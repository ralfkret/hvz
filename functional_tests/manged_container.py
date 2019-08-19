import logging
from collections import namedtuple
from contextlib import contextmanager

import docker
import psycopg2
from retry.api import retry_call


@contextmanager
def managed_container(image_name):
    """
    Start the container as specified by the image in a detachted state, with autoremove set.
    Yield the IP Address 
    Close the container when done 
    """
    cnt, ip_address = start_container(image_name)
    try:
        yield ip_address
    finally:
        logging.debug('Stopping container')
        cnt.stop()


def start_container(image_name, **kwargs):
    """
    Start a container from the image specified in a detached state, with autoremove set.
    Return the congtainer object and the IPAddress as a tuple.
    """
    dc = docker.from_env()
    logging.debug('Starting container')
    cnt = dc.containers.run(image_name, detach=True,
                            auto_remove=True, **kwargs)
    cnt.reload()
    ip_address = cnt.attrs['NetworkSettings']['IPAddress']
    logging.debug(f'IP of container: {ip_address}')
    Result = namedtuple("R", "container ip_address")
    dc.close()
    return Result(container=cnt, ip_address=ip_address)


def build_api_container():
    doc = docker.client.from_env()
    doc.images.build(path='api', tag='hvz-api')
    doc.close()


def wait_for_psql_container_ready(psql_server_ip_address):
    cn = retry_call(psycopg2.connect, fkwargs={
                    'host': psql_server_ip_address, 'user': 'postgres'}, tries=5, delay=0.5, backoff=2, logger=None)
    cn.close()


def create_sql_schema(psql_server_container, script='mnt/sql_scripts/create.sql'):
    result = psql_server_container.exec_run(
        cmd=f'psql -f {script}', user='postgres')
    if result.exit_code:
        raise RuntimeError('sql create script failed.\n' +
                           result.output.decode('utf-8'))
