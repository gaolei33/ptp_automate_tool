import logging
import os
import time
from webapp import config
from webapp.exceptions import PTPValueError
from webapp.util import io_util

__author__ = 'jonathan'

_logger = logging.getLogger('default')


def get_backup_list():
    backup_folder = config.BACKUP_FOLDER
    io_util.create_folder_if_not_exists(backup_folder)
    backup_list = [f for f in os.listdir(backup_folder) if os.path.isfile(os.path.join(backup_folder, f)) and f.lower().endswith('.sql.gz')]
    # sort by date reversed
    backup_list.sort(key=lambda x: os.path.getmtime(os.path.join(backup_folder, x)), reverse=True)
    return backup_list


def backup(sr_number):
    backup_folder = config.BACKUP_FOLDER
    io_util.create_folder_if_not_exists(backup_folder)

    current_time = time.strftime('%Y%m%d%H%M%S')
    backup_name = '[%s][DB_BACKUP]%s.sql.gz' % (sr_number, current_time)
    backup_path = os.path.join(backup_folder, backup_name)
    #backup_tables_string = ' '.join(config.BACKUP_TABLES)
    #cmd = 'mysqldump --no-autocommit -h %s -u %s -p%s %s %s | gzip > %s' % (config.DB_INFO['HOST'], config.DB_INFO['USER'], config.DB_INFO['PASSWORD'], config.DB_INFO['NAMES'], backup_tables_string, backup_path)
    cmd = 'mysqldump --no-autocommit -h %s -u %s -p%s %s | gzip > %s' % (config.DB['host'], config.DB['user'], config.DB['password'], config.DB['database'], backup_path)

    error = io_util.exec_cmd(cmd)

    if error:
        err_msg = 'An error occurred while backuping DB: %s' % error
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    _logger.info('DB backuped successfully.')


def restore(backup_name):
    backup_path = os.path.join(config.BACKUP_FOLDER, backup_name)

    if not os.path.exists(backup_path):
        err_msg = 'Backup file does not exist: %s' % backup_path
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    cmd = 'gunzip < %s | mysql -h %s -u %s -p%s %s' % (backup_path, config.DB['host'], config.DB['user'], config.DB['password'], config.DB['database'])

    error = io_util.exec_cmd(cmd)

    if error:
        err_msg = 'An error occurred while restoring DB: %s' % error
        _logger.error(err_msg)
        raise PTPValueError(err_msg)

    _logger.info('DB restored successfully.')


def delete_backup(backup_name):
    backup_path = os.path.join(config.BACKUP_FOLDER, backup_name)
    io_util.delete_file(backup_path)