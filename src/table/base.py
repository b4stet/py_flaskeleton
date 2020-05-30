class BaseTable():
    def __init__(self, db_connector, logger):
        self._logger = logger
        self.__db = db_connector
        self.__plans = []

    def _prepare_statement(self, plan, query):
        if plan not in self.__plans:
            self.__db.cursor().execute("PREPARE {} as {};".format(plan, query))
            self.__plans.append(plan)

    def _execute(self, plan, args=None):
        cursor = self.__db.cursor()

        if args is None:
            cursor.execute("EXECUTE {};".format(plan))
        else:
            pattern = '(' + ','.join(['%s']*len(args)) + ')'
            cursor.execute(
                "EXECUTE {} {};".format(plan, pattern),
                args
            )
        return cursor

    def _commit(self):
        self.__db.connection().commit()

    def _rollback(self):
        self.__db.connection().rollback()
