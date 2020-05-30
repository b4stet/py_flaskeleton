from flask import jsonify


class Response():
    def __init__(self, code, result):
        self.__code = code
        self.__result = result

    def to_json(self):
        response = {}
        response['result'] = self.__result
        response['code'] = self.__code
        response_json = jsonify(response)
        response_json.status_code = self.__code
        return response_json
