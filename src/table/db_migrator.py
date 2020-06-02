from src.table.abstract import AbstractTable
from src.entity.db_migrator import DbMigratorEntity


class DbMigratorTable(AbstractTable):
    def _dict2entity(self, record):
        if record is None:
            return None

        return DbMigratorEntity(
            migration_id=record['id'],
            filename=record['filename'],
            applied_at=record['applied_at']
        )

    def has_table(self):
        self._prepare_statement(
            'has_migration',
            "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='migration'"
        )
        result = self._execute('has_migration').fetchone()

        if result == [1]:
            return True
        else:
            return False

    def create_table(self):
        query = "CREATE TABLE migration ("
        query += "id SERIAL PRIMARY KEY,"
        query += "filename VARCHAR(255) UNIQUE NOT NULL,"
        query += "applied_at TIMESTAMP WITH TIME ZONE NOT NULL)"

        # because create/alter table statement cannot be prepared, directly execute
        self._cursor().execute(query)
        self._commit()

    def fetch_all(self):
        self._prepare_statement('select_migration_all', "SELECT * from migration")
        migrations = self._execute('select_migration_all').fetchall()

        results = [self._dict2entity(migration) for migration in migrations]
        return results

    def record_migration(self, migration: DbMigratorEntity):
        query = "INSERT INTO migration (filename, applied_at) VALUES ($1,$2)"
        params = [
            migration.get_filename(),
            migration.get_applied_at(),
        ]

        self._prepare_statement('insert_migration', query)
        self._execute('insert_migration', tuple(params))

    def apply_migration(self, migration_file):
        with open(migration_file, mode='r') as fsql:
            query = fsql.read()

        # because create/alter table statement cannot be prepared, directly execute
        self._cursor().execute(query)

    def finish_transaction(self, has_error):
        if has_error is True:
            self._rollback()
        else:
            self._commit()
