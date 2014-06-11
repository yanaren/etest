'''
Created on 2013-2-6

@author: renyong
'''
import os
import tempfile


def file_exist(file_name):
    return os.path.exists(file_name)


def folder_exist(folder):
    return file_exist(folder)


def create_file(file_name=None):
    if file_name:
        ab_path = os.path.abspath(file_name)
        parent_dir = os.path.split(ab_path)[0]
        if not folder_exist(parent_dir):
            os.makedirs(parent_dir)
        if not file_exist(ab_path):
            file_object = open(ab_path, 'w+')
            file_object.write('')
            file_object.close()
    else:
        # create a temp file for caller
        file_object = tempfile.NamedTemporaryFile(delete=False)
        file_name = file_object.name
        file_object.write('')
        file_object.close()
    return file_name


def write_to_file(to_file, content=''):
    if not file_exist(to_file):
        create_file(to_file)
    file_object = open(to_file, 'w+')
    file_object.write(content)
    file_object.close()


def write_to_tmp_file(content=''):
    file_name = create_file()
    write_to_file(file_name, content)
    return file_name


def append_to_file(to_file, content=''):
    if not file_exist(to_file):
        raise IOError('File "%s" not existed' % to_file)
    file_object = open(to_file, 'a+')
    file_object.write(content)
    file_object.close()


def read_file(file_name):
    '''
    read file content into a string object
    if file does not exist, an exception will be raised
    '''
    if not file_exist(file_name):
        raise IOError('File "%s" not existed' % file_name)

    file_object = open(file_name, 'r')
    file_content = file_object.read()
    return file_content


def read_file_into_lines(file_name, line_num=None):
    '''
    read file content into a list object
    if file does not exist, an exception will be raised
    line_num: if set, will read first line_num of file only
    '''
    if not file_exist(file_name):
        raise IOError('File "%s" not existed' % file_name)

    file_content = []
    file_object = open(file_name, 'r')
    if line_num:
        file_content = file_object.readlines(line_num)
    else:
        file_content = file_object.readlines()
    return file_content


def delete_file(file_name):
    if file_exist(file_name):
        os.remove(file_name)
