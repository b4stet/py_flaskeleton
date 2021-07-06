from flask import g
import psycopg2
import psycopg2.extras


class DbConnectorService():
    def __init__(self, config):
        self.__config = config
        self.__plans = []

    def connection(self):
        if 'db' not in g:
            g.db = psycopg2.connect(
                host=self.__config['host'],
                port=self.__config['port'],
                database=self.__config['name'],
                user=self.__config['user'],
                password=self.__config['password'],
            )
            cursor = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SET TIME ZONE 'UTC';")
            g.db.commit()
        return g.db

    def cursor(self):
        return self.connection().cursor(cursor_factory=psycopg2.extras.DictCursor)

    def disconnect(self, err):
        self.__plans = []
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def get_plans(self):
        return self.__plans

    def add_plan(self, plan):
        self.__plans.append(plan)
