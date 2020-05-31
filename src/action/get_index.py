from flask.views import MethodView

from src.template.response_web import Response


class GetIndexAction(MethodView):
    def __init__(self, logger):
        super().__init__()
        self._logger = logger

    def get(self):
        return Response(code=200, result='Flaskeleton says hi!').to_json(), 200
