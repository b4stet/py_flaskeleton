from src.middleware.user_authorization import UserAuthorizationMiddleware
from src.action.get_index import GetIndexAction
from src.action.list_users import ListUsersAction


routing = {
    'public': {
        'middlewares': [],
        'routes': [
            {
                'uri': '/',
                'action': GetIndexAction,
                'methods': ['GET'],
            },
        ],
    },

    'user': {
        'middlewares': [UserAuthorizationMiddleware],
        'routes': [
            {
                'uri': '/user/list',
                'action': ListUsersAction,
                'methods': ['GET'],
            },
        ]
    },
}
