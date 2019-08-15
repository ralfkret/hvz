from contextlib import contextmanager
from collections import namedtuple 
import docker
import logging

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
    cnt = dc.containers.run(image_name, detach=True, auto_remove=True, **kwargs)
    cnt.reload()
    ip_address = cnt.attrs['NetworkSettings']['IPAddress']
    logging.debug(f'IP of container: {ip_address}')
    Result = namedtuple("R", "container ip_address")
    return Result(container=cnt, ip_address=ip_address)
