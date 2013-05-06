from django.contrib import messages
from django.shortcuts import render
from webapp.manager import db_manager

__author__ = 'Gao Lei'


def db_home(request, method, description):
    backup_list = db_manager.get_backup_list()
    return render(request, 'db/db_home.html', {
        'backup_list': backup_list,
        'method': method,
        'description': description,
    })


def db_handler(request):
    try:
        method = request.POST['method'].strip()
        if method == 'DB_BACKUP':
            sr_number = request.POST['sr_number'].strip() or 'Unknown'
            db_manager.backup(sr_number)
            messages.info(request, 'Development Database backed up successfully.')
        elif method == 'DB_RESTORE':
            backup_name = request.POST['backup_name'].strip()
            if not backup_name:
                raise ValueError('Please select a valid DB backup file.')
            db_manager.restore(backup_name)
            messages.info(request, 'Development database restored successfully.')
        elif method == 'DB_BACKUP_DELETE':
            backup_name = request.POST['backup_name'].strip()
            if not backup_name:
                raise ValueError('Please select a valid DB backup file.')
            db_manager.delete_backup(backup_name)
            messages.info(request, 'DB Backup file deleted successfully.')
        else:
            messages.error(request, 'Invalid Operation.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')