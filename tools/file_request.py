"""
    File with function for reading file on the request
"""

import base64


def document_in_request(document, files):
    """
        Check if document is in request and convert to base64
    :param document: Document that you want to check
    :param files: Files from parameters
    :return:
    """
    if document in files:
        return base64_string(
            files['{}'.format(document)].file)
    return False


def base64_string(file):
    """
    Encodes file to base64 string.
    :param file: File
    :return: Base64 string
    """
    return base64.b64encode(file.read()).decode("utf-8")
