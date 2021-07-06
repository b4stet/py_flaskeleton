from abc import ABC, abstractmethod


class AbstractTable(ABC):
    def __init__(self, db_connector, logger):
        self._logger = logger
        self.__db = db_connector

    @abstractmethod
    def _dict2entity(self, record):
        raise NotImplementedError('The object must implement  _dict2entity method.')

    def _prepare_statement(self, plan, query):
        if plan not in self.__db.get_plans():
            self.__db.cursor().execute("PREPARE {} as {};".format(plan, query))
            self.__db.add_plan(plan)

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

    def _cursor(self):
        return self.__db.cursor()

    def _commit(self):
        self.__db.connection().commit()

    def _rollback(self):
        self.__db.connection().rollback()
