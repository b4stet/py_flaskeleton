from flask.views import MethodView

from src.template.response_web import Response


class ListUsersAction(MethodView):
    def __init__(self, user_bo, logger):
        super().__init__()
        self.__logger = logger
        self.__user_bo = user_bo

    def get(self):
        users = self.__user_bo.get_all()
        result = [self.__user_bo.entity2dict(user) for user in users]

        return Response(code=200, result=result).to_json(), 200
