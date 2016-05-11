import sqlite3;

class DALException(Exception):
    pass

class BadRequirementsError(DALException):
    pass

class FieldRequiredError(DALException):
    pass

class FieldNotNullableError(DALException):
    pass

class Sqlite3Base():
    def __init__(self, config):
        # TODO - should try/except here
        self._db_conn = sqlite3.connect(config['dbpath'])
        self._db_conn.row_factory = sqlite3.Row
        self._table_prefix = ''
        if ( 'prefix' in config ):
            self._table_prefix = config['prefix'] + '_'
            
    def test_fields(self, requirements, values):
        field_dict = dict()
        for field, requirement in requirements.items():
            if ( requirement == 'req'):
                if ( field not in values ):
                    raise FieldRequiredError
                field_dict[field] = values[field]
            elif ( requirement == 'reqnotnull' ):
                if ( field not in values ):
                    raise FieldRequiredError
                if ( values[field] is None ):
                    raise FieldNotNullableError
                field_dict[field] = values[field]
            elif ( requirement == 'notreqnotnull' ):
                if ( field in values ):
                    if ( values[field] is None ):
                        raise FieldNotNullableError
                    field_dict[field] = values[field]
            elif ( requirement == 'notreq' ):
                if ( field in values ):
                    field_dict[field] = values[field]
            else:
                raise BadRequirementsError
            # Note: we don't care if extra fields are in values;
            # that can actually be useful in some cases - insert from returned field_dict
        return field_dict
    
    def db_finish(self):
        self._db_conn.close()