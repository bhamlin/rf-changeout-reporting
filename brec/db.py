
class DatabaseConnection:
    pass

class PostgreSQL(DatabaseConnection):
    def __init__(self, dsn=None):
        self.DEBUG = False
        self._pg = __import__('psycopg2')
        self._dict_cur = __import__('psycopg2.extras', fromlist=['RealDictCursor']).RealDictCursor
        if dsn:
            self.connect(dsn)
    
    def _get_cursor(self):
        return self._db.cursor(cursor_factory=self._dict_cur)

    def _nuke_from_orbit(self):
        with self._get_cursor() as cur:
            cur.execute(''' truncate hunt.rf_changeout_data cascade ''')
            cur.execute('commit transaction')
            cur.execute(''' SELECT setval('hunt.rf_changeout_data_id_seq', 1, true) ''')
            cur.execute(''' SELECT setval('hunt.rf_changeout_loc_id_seq', 1, true) ''')
            cur.execute(''' SELECT setval('hunt.rf_changeout_photos_id_seq', 1, true) ''')
            cur.execute(''' SELECT setval('hunt.rf_changeout_site_insp_id_seq', 1, true) ''')
            cur.execute(''' VACUUM FULL hunt.rf_changeout_data ''')
            cur.execute(''' VACUUM FULL hunt.rf_changeout_loc ''')
            cur.execute(''' VACUUM FULL hunt.rf_changeout_photos ''')
            cur.execute(''' VACUUM FULL hunt.rf_changeout_site_insp ''')
    
    def close(self):
        self._db.close()
    
    def connect(self, dsn):
        self._db = self._pg.connect(dsn)
        if self.DEBUG:
            self._nuke_from_orbit()

    def execute(self, query):
        with self._get_cursor() as cur:
            cur.execute(query)
            for record in cur:
                yield record

    def execute_args(self, query, *args):
        with self._get_cursor() as cur:
            cur.execute(query, args)
            for record in cur:
                yield record

    def execute_crud(self, query):
        with self._get_cursor() as cur:
            cur.execute(query)
            cur.execute('commit transaction')

    def execute_crud_args(self, query, *args):
        with self._get_cursor() as cur:
            cur.execute(query, args)
            cur.execute('commit transaction')
