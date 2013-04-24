import logging
import os
import time
from webapp import config
from webapp.common.io import io_utils

__author__ = 'jonathan'

_logger = logging.getLogger('default')

def get_backup_list():

    backup_folder = config.BACKUP_FOLDER
    io_utils.create_folder_if_not_exists(backup_folder)

    return [f for f in os.listdir(backup_folder) if os.path.isfile(os.path.join(backup_folder, f)) and f.lower().endswith('.sql.gz')]


def backup(sr_number):

    backup_folder = config.BACKUP_FOLDER
    io_utils.create_folder_if_not_exists(backup_folder)

    current_time = time.strftime('%Y%m%d%H%M%S')
    backup_name = 'SR_%s_dev_db_backup_%s.sql.gz' % (sr_number, current_time)
    backup_path = os.path.join(backup_folder, backup_name)
    cmd = 'mysqldump -h %s -u %s -p%s %s %s | gzip > %s' % (
    config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'], config.BACKUP_TABLES, backup_path)

    error = io_utils.exec_cmd(cmd)

    if error:
        err_msg = 'An error occurred while backing up development database: %s' % error
        _logger.error('Dev DB restore fail: ' + error)
        raise ValueError(err_msg)

    _logger.info('Development database backed up successfully.')


def restore(backup_name):

    backup_folder = config.BACKUP_FOLDER
    backup_path = os.path.join(backup_folder, backup_name)

    if not os.path.exists(backup_path):
        err_msg = 'Backup file does not exist: %s' % backup_path
        _logger.error(err_msg)
        raise ValueError(err_msg)

    cmd = 'gunzip < %s | mysql -h %s -u %s -p%s %s' % (backup_path, config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAME'])

    error = io_utils.exec_cmd(cmd)

    if error:
        err_msg = 'An error occurred while restoring development database: %s' % error
        _logger.error('Dev DB restore fail: ' + error)
        raise ValueError(err_msg)

    _logger.info('Development database restored successfully.')