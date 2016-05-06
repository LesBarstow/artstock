import importlib

class Works():
    
    dbaccess = None
    works_dbh = None
    
    def __init__(self, config):
        dbtype = 'sqlite3'
        if ( 'dbtype' in config):
            dbtype = config['dbtype']
        self.dbaccess = importlib.import_module(dbtype + '.works')
        self.works_dbh = self.dbaccess.Works(config)
    
    def create(self, values):
        self.works_dbh.create(values)
    
    def delete(self, values):
        self.works_dbh.delete(values)
        
    def retrieve(self, values):
        return self.works_dbh.retrieve(values)