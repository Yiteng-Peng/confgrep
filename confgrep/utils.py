import os
import uuid
import logging
import tempfile
from contextlib import contextmanager

import colorlog

from .config import *

# color and format
logger_formatter = colorlog.ColoredFormatter(
    '[%(name)s][%(levelname)s]%(asctime)s %(log_color)s%(message)s',
    datefmt='%m-%d %H:%M')

def new_logger(name, level='DEBUG', new=True):
    # add custom level "VERBOSE"
    VERBOSE = 5
    logging.addLevelName(VERBOSE, "VERBOSE")
    logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(VERBOSE, msg, *args, **kwargs)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logger_formatter)

    logger = logging.getLogger(name)
    if new: logger.handlers = []

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

@contextmanager
def path_context(path):
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(cwd)

@contextmanager
def tmpdir_ctx():
    try:
        tmpdir = tempfile.mkdtemp()
        yield tmpdir
    finally:
        os.system("rm -rf %s" % tmpdir)

@contextmanager
def tmpfile_ctx(prefix=None):
    fname = str(uuid.uuid4())
    if prefix:
        fpath = os.path.join(prefix, fname)
    else:
        fpath = fname
    fpath = os.path.abspath(fpath)


    try:
        os.system("touch %s" % fpath)
        yield fpath
    finally:
        os.system("rm %s" % fpath)


def handle_field_str(field_str):
    field = [s.strip().upper() for s in field_str.split(",")]
    return field

def get_conf_list(field):
    conf_list = []
    if "ALL" in field:
        conf_list = ALL_CONFERENCES_LIST
    else:
        for field_name in field:
            try:
                conf_list.extend(CONFERENCES[field_name])
            except KeyError:
                print(f"No such field {field_name}! Pass.")
        conf_list = list(set(conf_list))
    return conf_list
    