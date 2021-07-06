from flask import current_app
from werkzeug.exceptions import default_exceptions
import sys
import traceback

from src.template.response_web import Response


class ErrorHandlerService():
    def __init__(self):
        self.__logger = current_app.logger
        self.__env = current_app.config['env']

    def init_app(self, app):
        app.register_error_handler(Exception, self.handler)
        for code, _ in default_exceptions.items():
            app.register_error_handler(code, self.handler)

    def handler(self, error):
        response = None

        status_code = 500
        if hasattr(error, 'code'):
            status_code = error.code

        # format of log line
        stack = traceback.format_tb(sys.exc_info()[2])
        error_location = stack[-1].split('\n')[0].strip(' ')
        error_type = type(error).__name__
        error_value = str(error).split('\n')[0]
        error_log = '[{}] {}: {}'.format(error_location, error_type, error_value)

        # logging: full stack trace
        # 4xx as warning
        # 5xx as error
        if 500 <= status_code < 600:
            self.__logger.error(error_log, exc_info=True)
        else:
            self.__logger.warning(error_log, exc_info=True)

        # reponse
        response = Response(code=status_code, result=str(error))
        if 500 <= status_code < 600:
            response = Response(code=status_code, result='Server error.')

        return response.to_json(), status_code
