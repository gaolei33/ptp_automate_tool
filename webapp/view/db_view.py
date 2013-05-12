from django.contrib import messages
from django.shortcuts import render
from webapp.exceptions import PTPValueError
from webapp.manager import db_manager
from webapp.view import GlobalErrorHandler

__author__ = 'Gao Lei'


@GlobalErrorHandler
def db_home(request, method, description):
    backup_list = db_manager.get_backup_list()
    return render(request, 'db/db_home.html', {
        'backup_list': backup_list,
        'method': method,
        'description': description,
    })


@GlobalErrorHandler
def db_handler(request):
    method = request.POST['method'].strip()
    if method == 'DB_BACKUP':
        sr_number = request.POST['sr_number'].strip() or 'Unknown'
        db_manager.backup(sr_number)
        messages.info(request, 'DB backuped successfully.')
    elif method == 'DB_RESTORE':
        backup_name = request.POST['backup_name'].strip()
        if not backup_name:
            raise PTPValueError('Please select a valid DB backup file.')
        db_manager.restore(backup_name)
        messages.info(request, 'DB restored successfully.')
    elif method == 'DB_BACKUP_DELETE':
        backup_name = request.POST['backup_name'].strip()
        if not backup_name:
            raise PTPValueError('Please select a valid DB backup file.')
        db_manager.delete_backup(backup_name)
        messages.info(request, 'DB backup file deleted successfully.')
    else:
        messages.error(request, 'Invalid Operation.')

    return render(request, 'common/result.html')