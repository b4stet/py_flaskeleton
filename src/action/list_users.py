from flask.views import MethodView

from src.template.response_web import Response


class ListUsersAction(MethodView):
    def __init__(self, time_converter, user_bo, logger):
        super().__init__()
        self.__logger = logger
        self.__time_converter = time_converter
        self.__user_bo = user_bo

    def get(self):
        users = self.__user_bo.get_all()

        result = []
        for user in users:
            result.append({
                'name': user.get_name(),
                'status': user.get_status(),
                'created_at': self.__time_converter.to_str(user.get_created_at()),
                'modified_at': self.__time_converter.to_str(user.get_modified_at()),
            })

        return Response(code=200, result=result).to_json(), 200
