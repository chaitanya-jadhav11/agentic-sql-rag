from core.db import db

_schema_cache = None


def get_cache_db_schema():
    global _schema_cache

    if _schema_cache is None:
        print("Loading schema from DB...")
        table_names = db.get_usable_table_names()

        _schema_cache = "\n\n".join(
            db.get_table_info([table])
            for table in table_names
        )

    return _schema_cache