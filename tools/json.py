"""

    Json file: Create and set a json object for the routes

"""

import json


class ApiJsonResponse():
    """
    Class returning a json containing a result code, a result message
    a boolean True or False and datas.
    """

    def __init__(self):
        """
        init class
        """
        self._dict = {
            'status': '',
            'msg': '',
            'is_error': 0,
            'result_data': []
        }

    def set_result_code(self, result_code):
        """
        function setting the result code
        :param result_code: result code of the function
        :return: a json dictionnary with the result code set
        """
        self._dict['status'] = result_code

    def set_result_msg(self, result_msg):
        """
        function setting the result message
        :param result_msg: result message of the function
        :return: a json dictionnary with the result message set
        """
        self._dict['msg'] = result_msg

    def set_error(self, an_error):
        """
        function setting the error if an error exist
        :param an_error: boolean true if an error exist or false
        :return: a json dictionnary with the error code set
        """
        self._dict['is_error'] = an_error

    def set_data(self, data):
        """
        function setting the datas
        :param data: string of datas
        :return: a json dictionnary with the datas set
        """
        self._dict['result_data'] = data

    def set_multiples_data(self, data):
        """
        function setting the datas
        :param data: string of datas
               data_name: name of the data
        :return: a json dictionnary with the datas set
        """
        self._dict['result_data'].append(data)
#        self._dict[data_name] = data

    def get_dict(self):
        """
        function setting the result code
        :return: a json dictionnary
        """
        return self._dict

    def dump(self, fp, **kwargs):
        """
        function serialize an existing object with the dictionnary
        :param fp: existing json object
         **kwargs: new args for the json object
        :return: a json object
        """
        json.dumps(self._dict, fp, **kwargs)

    def dumps(self, **kwargs):
        """
        function serialize args of the dictionnary
        :param **kwargs: args for the json object
        :return: a json object
        """
        return json.dumps(self._dict, **kwargs)
