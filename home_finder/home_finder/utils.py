# -*- coding: utf-8 -*-

import dropbox


def get_dropbox_object(token):
    dbx = dropbox.Dropbox(token)
    return dbx


def dropbox_file_exists(dbx, path):
    try:
        metadata = dbx.files_get_metadata(path)
        return True
    except dropbox.exceptions.ApiError:
        return False


def dropbox_create_file(dbx, path, data):
    data = "\n".join(data)
    data_as_bytes = str.encode(data)
    dbx.files_upload(data_as_bytes, path)


def dropbox_delete_file(dbx, path):
    dbx.files_delete(path)


def dropbox_load_file(dbx, path):
    md, res = dbx.files_download(path)
    data_as_str = res.content.decode()
    return data_as_str
