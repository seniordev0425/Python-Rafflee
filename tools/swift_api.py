"""
    Swift API functions
"""

import glob
import os
import logging
import json
import base64

from rafflee import settings
from swiftclient import ClientException
from swiftclient.client import Connection

logger = logging.getLogger(__name__)


def get_swift_connection_userdocs():
    """
    Function which returns a connection to a swift object storage
    :return connection: connection to swift
    :rtype connection: swiftclient.client.Connection
    """
    swift = Connection(authurl=settings.OS_AUTH_URL,
                       user=settings.OS_USERNAME,
                       key=settings.OS_PASSWORD,
                       tenant_name=settings.OS_TENANT_NAME,
                       auth_version=settings.OS_IDENTITY_API_VERSION,
                       os_options=settings.OS_OPTIONS)
    return swift


def delete_user_docs(path):
    """
    Delete a user document on disk or in object storage, depending of
    configuration
    :param path: path of file
    :type path: string
    :param data: data to write in file
    :type data: str
    :raises: ClientException
    """
    if not settings.SWIFT_USERFILES:
        # Use filesystem
        logger.debug('delete user document on filesystem in "%s"', path)
        path = '{}*'.format(path)
        list_of_files = glob.glob(
            os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), settings.FOLDER_DOCS) + path)
        latest_file = max(list_of_files, key=os.path.getctime)
        try:
            os.remove(latest_file)
        except FileExistsError:
            # directory already exists
            pass
    else:
        # Use swift object storage
        logger.debug('delete user document in swift at "%s"', path)
        swift = get_swift_connection_userdocs()
        try:
            # first, select the last object with path a prefix
            objects = swift.get_container(
                settings.OS_CONTAINER, prefix=path, full_listing=True)
            objects = [object['name'].split('/')[-1] for object in objects[1]]
            objects.sort(reverse=True)

            # now, retrieve the object content
            path = '{}{}'.format(path, objects[0])
            response = swift.delete_object(settings.OS_CONTAINER, path)
            response[1].decode('utf-8')
        except ClientException:
            logger.warning('unable to get user doc object in swift container "%s" at "%s"',
                           settings.OS_CONTAINER, path)
            return None
        except IndexError:
            logger.warning('unable to get user doc object in swift container "%s" at "%s"',
                           settings.OS_CONTAINER, path)
            return None


def write_user_docs(path, data):
    """
    Write a user document on disk or in object sotrage, depending of
    configuration
    :param path: path of file
    :type path: string
    :param data: data to write in file
    :type data: str
    :raises: ClientException
    """
    if not settings.SWIFT_USERFILES:
        # Use filesystem
        logger.debug('write user document on filesystem in "%s"', path)
        try:
            os.makedirs('/'.join(path.split('/')[:-1]))
        except FileExistsError:
            # directory already exists
            pass
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
    else:
        # Use swift object storage
        logger.debug('write user document in swift at "%s"', path)
        path = path.replace(settings.FOLDER_DOCS, '')
        swift = get_swift_connection_userdocs()
        try:
            # we always push an empty object at "/<pikcioid>" to
            # ensure that is user has already pushed files
            swift.put_object(settings.OS_CONTAINER,
                             '{}/{}/{}'.format(settings.FOLDER_DOCS, path.split('/')[1], path.split('/')[2]),
                             contents='',
                             content_type='text/plain')
            # now, we can push the real document
            data = base64.b64decode(data)
            swift.put_object(settings.OS_CONTAINER, settings.FOLDER_DOCS + path,
                             contents=data,
                             content_type='image/png')
            return (swift.url + '/' + settings.OS_CONTAINER + '/' + settings.FOLDER_DOCS + path)
        except ClientException as e:
            logger.error('unable to put object in swift container "%s" at "%s"',
                         settings.OS_CONTAINER, path)
            raise e


def read_last_user_docs(path):
    """
    Read a user document (the most recent) (last) on disk or in object sotrage, depending of
    configuration
    :param path: path of file
    :type path: string
    :return data: content of file
    :rtype data: string
    """
    data = ''
    if not settings.SWIFT_USERFILES:
        logger.debug('read user document on filesystem in "%s"', path)
        path = '{}*'.format(path)
        list_of_files = glob.glob(
            os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), settings.FOLDER_DOCS) + path)
        latest_file = max(list_of_files, key=os.path.getctime)
        data = open(latest_file, "r").read()
    else:
        # Use swift object storage
        logger.debug('read user document in swift at "%s"', path)
        swift = get_swift_connection_userdocs()
        try:
            # first, select the last object with path a prefix
            objects = swift.get_container(
                settings.OS_CONTAINER, prefix=path, full_listing=True)
            objects = [object['name'].split('/')[-1] for object in objects[1]]
            objects.sort(reverse=True)
            # now, retrieve the object content
            url = swift.url + '/' + settings.OS_CONTAINER + '/' + path + objects[0]
            return url
        except ClientException as e:
            logger.warning('unable to get user doc object in swift container "%s" at "%s"',
                           settings.OS_CONTAINER, path)
            return None
        except IndexError as e:
            logger.warning('unable to get user doc object in swift container "%s" at "%s"',
                           settings.OS_CONTAINER, path)
            return None


def check_user_docs(path):
    """
    Check if user documents folder exists on disk or in object storage,
    depending of configuration
    :param path: path of user folder
    :type path: string
    :return: if folder exists
    :rtype: bool
    """
    if not settings.SWIFT_USERFILES:
        logger.debug('check if user folder exists on filesystem')
        user_docs = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), settings.FOLDER_DOCS) + path
        return os.path.exists(user_docs)
    else:
        # Use swift object storage
        # ensure to remove wrong slash
        swift = get_swift_connection_userdocs()
        path = path.replace('/', '')
        path = '/{}'.format(path)
        logger.debug('check if user folder exists in swift at "%s"', path)
        try:
            swift.get_object(settings.OS_CONTAINER, path)
        except ClientException:
            logger.warning('unable to get user doc object in swift container "%s" at "%s"',
                           settings.OS_CONTAINER, path)
            return False
        return True