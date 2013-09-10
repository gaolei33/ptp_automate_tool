from StringIO import StringIO
import os
import re
from zipfile import ZipFile
from webapp import config

__author__ = 'Gao Lei'


def _get_filename_from_path(path):
    filename_index = path.rfind('/') + 1
    return path[filename_index:]


def _pdf_rename(pdf_name_origin):
    return re.sub(config.PDF_RENAME_PATTERN, '', pdf_name_origin)


def pdf_rename(file_origin):
    file_target = StringIO()
    with ZipFile(file_origin, 'r') as zip_origin, ZipFile(file_target, 'w') as zip_target:
        for pdf_path_origin in zip_origin.namelist():
            if pdf_path_origin.lower().endswith('.pdf'):
                pdf_name_origin = _get_filename_from_path(pdf_path_origin)
                pdf_name_target = _pdf_rename(pdf_name_origin)
                pdf_path_target = os.path.join(config.PDF_ROOT, pdf_name_target)
                zip_target.writestr(pdf_path_target, zip_origin.read(pdf_path_origin))
    file_content_target = file_target.getvalue()
    file_target.close()

    return file_content_target


def main():
    with file('/home/jonathan/Desktop/pdf.zip', 'r') as zip_origin, file('/home/jonathan/Desktop/pdf_target.zip', 'w') as zip_target:
        file_content_target = pdf_rename(zip_origin)
        zip_target.write(file_content_target)


if __name__ == '__main__':
    main()