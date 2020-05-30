import os
import sys
from datetime import datetime, timezone

from src.entity.db_migrator import DbMigratorEntity


class DbMigratorBo():
    def __init__(self, migrator_table, logger):
        self.__logger = logger
        self.__migrator_table = migrator_table

    def compare(self, migration_path):
        # applied migrations, from db
        from_db = self.__migrator_table.fetch_all()
        migrated = [migration.get_filename() for migration in from_db]

        # available migrations, from application folder
        migrations = []
        for f in os.listdir(migration_path):
            if os.path.isfile(os.path.join(migration_path, f)) and f.endswith('.sql'):
                migrations.append(f)

        # get the diff
        result = [migration for migration in migrations if migration not in migrated]
        result.sort(key=lambda m: m.split('_')[0])
        return result

    def init(self):
        is_initialized = self.__migrator_table.has_table()

        if is_initialized is False:
            self.__migrator_table.create_table()
            return True

        return False

    def apply(self, migration_path, filenames):
        in_progress = None
        try:
            for filename in filenames:
                in_progress = filename

                # apply content of sql file
                migration_file = os.path.join(migration_path, filename)
                self.__migrator_table.apply_migration(migration_file)

                # record that migration was applied
                migration = DbMigratorEntity(
                    filename=filename,
                    applied_at=datetime.now(timezone.utc),
                )
                self.__migrator_table.record_migration(migration)
        except Exception as err:
            self.__logger.warning('[DB] error: {}'.format(str(err)))
            self.__migrator_table.finish_transaction(has_error=True)
            return False, in_progress

        self.__migrator_table.finish_transaction(has_error=False)
        return True, None
