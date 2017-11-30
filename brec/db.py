
class DatabaseConnection:
    pass

class PostgreSQL(DatabaseConnection):
    def __init__(self, dsn=None):
        self._pg = __import__('psycopg2')
        if dsn:
            self.connect(dsn)
    
    def connect(self, dsn):
        self._db = self._pg.connect(dsn)
