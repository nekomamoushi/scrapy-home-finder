# -*- coding: utf-8 -*-

import os
import csv

import dropbox
import yaml
import requests

def retrieve_environ(name):
    environ = os.environ.get(name, None)
    if not environ:
        raise Exception("You need to set {name}".format(name=name))
    return environ


def yaml_load(dropbox, filename):
    if not dropbox_file_exists(dropbox, filename):
        error_msg = "Dropbox: <{0}> don't exists.".format(filename)
        raise Exception(error_msg)
    data = dropbox_load_file(dropbox, filename)
    return yaml.safe_load(data)


def csv_load(filename, delimiter=';'):
    with open(filename, mode='r') as fp:
        csv_reader = csv.reader(fp, delimiter=delimiter)
        data = [row for row in csv_reader]
    return data


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


class Notifier(object):

    NOTIFY_URL = "https://maker.ifttt.com/trigger/{0}/with/key/{1}"

    def __init__(self, credentials, trigger):
        self._credentials = credentials
        self._trigger = trigger

    def process_data(self, data):
        payload = dict(
            value1=data["city"],
            value2=data["price"],
            value3=data["url"]
        )
        return payload

    def send(self, data):
        url = self.NOTIFY_URL.format(self._trigger, self._credentials)
        r = requests.post(url, data=data)
        self.logger.debug("http status: <{0}>".format(r.status_code))

    def notify(self, data):
        data = self.process_data(data)
        self.send(data)
