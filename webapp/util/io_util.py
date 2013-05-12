import logging
import os
import subprocess
from webapp.exceptions import PTPValueError

__author__ = 'Gao Lei'

_logger = logging.getLogger('default')


def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            _logger.info('Folder created successfully: %s' % folder)
        except Exception, ex:
            err_msg = 'An error occurred while creating folder %s: %s' % (folder, ex)
            _logger.error(err_msg)
            raise PTPValueError(err_msg)


def write_to_file(file_path, obj):
    try:
        file_dir = os.path.dirname(file_path)
        create_folder_if_not_exists(file_dir)

        with open(file_path, 'w') as target_file:
            if type(obj) in (str, unicode):
                    target_file.write(obj)
            else:
                for chunk in obj.chunks():
                    target_file.write(chunk)

        _logger.info('File created successfully: %s' % file_path)
    except Exception, ex:
            err_msg = 'An error occurred while writing file %s: %s' % (file_path, ex)
            _logger.error(err_msg)
            raise PTPValueError(err_msg)


def delete_file(file_path):
    if not os.path.exists(file_path):
        err_msg = 'File does not exist: %s' % file_path
        _logger.error(err_msg)
        raise PTPValueError(err_msg)
    try:
        os.remove(file_path)
    except Exception, ex:
        err_msg = 'An error occurred while deleting file %s: %s' % (file_path, ex)
        _logger.error(err_msg)
        raise PTPValueError(err_msg)


def exec_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = process.stdout.read()
    return result