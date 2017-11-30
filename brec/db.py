
class DatabaseConnection:
    pass

class PostgreSQL(DatabaseConnection):
    def __init__(self, dsn=None):
        self._pg = __import__('psycopg2')
        self._dict_cur = __import__('psycopg2.extras', fromlist=['RealDictCursor']).RealDictCursor
        if dsn:
            self.connect(dsn)
    
    def _get_cursor(self):
        return self._db.cursor(cursor_factory=self._dict_cur)
    
    def close(self):
        self._db.close()
    
    def connect(self, dsn):
        self._db = self._pg.connect(dsn)

    def execute(self, query):
        cur = self._get_cursor()
        cur.execute(query)
        for record in cur:
            yield record
        cur.close()
