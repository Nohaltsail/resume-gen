from resume.service.manager import service_registry

mysqldb = service_registry.get_mysql_service(name="default_db", namespace="default")
sqlitedb = service_registry.get_sqlite_service(name="sqlite_db", namespace="local")


def get_mysql_db():
    db = mysqldb.client.get_session()
    try:
        yield db
    finally:
        db.close()


def get_sqlite_db():
    db = sqlitedb.client.get_session()
    try:
        yield db
    finally:
        db.close()

