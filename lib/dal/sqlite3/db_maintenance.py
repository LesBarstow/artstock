import os;
import os.path;
import sqlite3;

class DbMaintenance():
    
    def __init__(self, config):
        if ( config['force'] ):
            if ( os.path.exists(config['dbpath']) ):
                if ( os.path.isfile(config['dbpath']) ):
                    try:
                        os.unlink(config['dbpath'])
                    except Exception as e:
                        raise FileExistsError
                else:
                    raise FileExistsError
        # Don't continue if there's already a file there!
        if ( os.path.exists(config['dbpath']) ):
            raise FileExistsError
        # TODO - should try/except here
        self._db_conn = sqlite3.connect(config['dbpath'])
        self._table_prefix = ''
        if ( 'prefix' in config ):
            self._table_prefix = config['prefix'] + '_'

    def drop_tables(self):
        self.drop_works()
    
    def create_tables(self):
        self.create_works()
    
    def create_works(self):
        cw_cur = self._db_conn.cursor()
        cw_cur.execute(
            "CREATE TABLE " + self._table_prefix + "works" """\
            (
                work_id          VARCHAR(255) NOT NULL PRIMARY KEY,
                title            VARCHAR(255),
                description      VARCHAR(2048),
                work_created_ts  INTEGER,
                inserted_ts      INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """)
        self._db_conn.commit()
    
    def drop_works(self):
        cw_cur = self._db_conn.cursor()
        cw_cur.execute("DROP TABLE " + self._table_prefix + "works")
    
    def db_finish(self):
        self._db_conn.close()