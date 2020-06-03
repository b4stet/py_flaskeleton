class DbMigratorEntity():
    def __init__(self, filename, applied_at, migration_id=None):
        self.__id = migration_id
        self.__filename = filename
        self.__applied_at = applied_at

    def get_id(self):
        return self.__id

    def get_filename(self):
        return self.__filename

    def get_applied_at(self):
        return self.__applied_at

    def to_dict(self):
        return {
            'id': self.__id,
            'filename': self.__filename,
            'applied_at': self.__applied_at
        }
