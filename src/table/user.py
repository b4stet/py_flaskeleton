from src.table.abstract import AbstractTable
from src.entity.user import UserEntity


class UserTable(AbstractTable):
    def __init__(self, crypter, hasher, db_connector, logger):
        super().__init__(db_connector, logger)
        self.__crypter = crypter
        self.__hasher = hasher

    def _dict2entity(self, record):
        if record is None:
            return None

        name = self.__crypter.decrypt(record['name_encrypted'], record['nonce'])

        return UserEntity(
            user_id=record['id'],
            name=name,
            password=record['password'],
            salt=record['salt'],
            status=record['status'],
            created_at=record['created_at'],
            modified_at=record['modified_at'],
        )

    def save(self, user: UserEntity):
        # no id: it's a new record
        if user.get_id() is None:
            name_encrypted, nonce = self.__crypter.encrypt(user.get_name())
            name_hashed = self.__hasher.anonymize(user.get_name())

            query = "INSERT INTO user_account (name_hashed, name_encrypted, salt, nonce, password, status, created_at, modified_at) "
            query += "VALUES ($1,$2,$3,$4,$5,$6,$7,$8)"
            params = [name_hashed, name_encrypted, user.get_salt(), nonce, user.get_password()]
            params += [user.get_status(), user.get_created_at(), user.get_modified_at()]
            self._prepare_statement('insert_user', query)
            self._execute('insert_user', tuple(params))

        # id: it's an update
        else:
            query = "UPDATE user_account SET password=$1, salt=$2, status=$3, modified_at=$4 WHERE id=$5"
            params = [user.get_password(), user.get_salt(), user.get_status(), user.get_modified_at(), user.get_id()]
            self._prepare_statement('update_user', query)
            self._execute('update_user', tuple(params))

        self._commit()
        return self.fetch_by_name(user.get_name())

    def fetch_all(self):
        query = "SELECT * FROM user_account"
        self._prepare_statement('select_user_all', query)
        records = self._execute('select_user_all').fetchall()
        results = [self._dict2entity(record) for record in records]
        return results

    def fetch_by_name(self, name):
        name_hashed = self.__hasher.anonymize(name)
        query = "SELECT * FROM user_account WHERE name_hashed=$1"
        params = [name_hashed]
        self._prepare_statement('select_user_by_name', query)
        record = self._execute('select_user_by_name', tuple(params)).fetchone()

        return self._dict2entity(record)

    def fetch_by_id(self, user_id):
        query = "SELECT * FROM user_account WHERE id=$1"
        params = [user_id]
        self._prepare_statement('select_user_by_id', query)
        record = self._execute('select_user_by_id', tuple(params)).fetchone()

        return self._dict2entity(record)
