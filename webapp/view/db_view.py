from django.contrib import messages
from django.shortcuts import render
from webapp.manager import db_manager

__author__ = 'Gao Lei'


def db_home(request):
    backup_list = db_manager.get_backup_list()
    return render(request, 'db/db_home.html', {
        'backup_list': backup_list,
    })


def db_backup(request):
    try:
        sr_number = request.POST['sr_number'].strip() or 'Unknown'
        db_manager.backup(sr_number)
        messages.info(request, 'Development Database backed up successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')


def db_restore(request):
    try:
        backup_name = request.POST['backup_name'].strip()

        if not backup_name:
            raise ValueError('Please select a valid DB backup file.')

        db_manager.restore(backup_name)

        messages.info(request, 'Development database restored successfully.')
    except KeyError, ex:
        messages.error(request, ex)
    except ValueError, ex:
        messages.error(request, ex)
    return render(request, 'common/result.html')
