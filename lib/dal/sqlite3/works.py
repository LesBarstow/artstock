from dal.sqlite3.sqlite3base import Sqlite3Base

import json # for debugging

class Works(Sqlite3Base):
    def create(self, values):
        requirements = {
            'work_id': 'reqnotnull',
            'title': 'notreq',
            'description': 'notreq',
            'work_created_ts': 'notreq'
        }
        field_dict = self.test_fields(requirements, values)
        field_list = list(field_dict.keys())
        # Happy auto-generating variable field name with named bind SQL generator
        create_sql =  (
            "INSERT INTO " + self._table_prefix + "works "
            "(" + ", ".join(field_list) + ") "
            "VALUES (:" + ", :".join(field_list) + ")" 
        )
        create_cur = self._db_conn.cursor()
        create_cur.execute(create_sql, field_dict)
        self._db_conn.commit()
    
    def delete(self, values):
        requirements = {
            'works_id': 'reqnotnull'
        }
        field_dict = self.test_fields(requirements, values)
        field_list = list(field_dict.keys())
        delete_sql = (
            "DELETE FROM " + self._table_prefix + "works "
            "WHERE works_id = :works_id"
        )
        # field_dict now becomes our named parameter dict
        for field in field_list:
            field_dict[":"+field] = field_dict.pop(field)
        delete_cur = self._db_conn.cursor()
        delete_cur.execute(delete_sql, field_dict)
        self._db_conn.commit()
    
    def retrieve(self, values):
        requirements = {
            'work_id': 'notreqnotnull',
            'title': 'notreq',
            'description': 'notreq',
            'work_created_ts': 'notreq',
            'inserted_ts': 'notreq',
            "join_type": "notreqnotnull",
            "match_type": "notreqnotnull"
        }
        field_dict = self.test_fields(requirements, values)
        join_type = " AND "
        if ( "join_type" in field_dict):
            join_type = field_dict.pop("join_type").lower()
            if ( join_type == "or" ):
                join_type = " OR "
            else:
                join_type = " AND "
        match_type = "exact"
        if ( "match_type" in field_dict ):
            match_type = field_dict.pop("match_type").lower()
            if ( match_type != "contains" ):
                match_type = "exact"
        clauses = list()
        if ( "work_id" in field_dict):
            if ( match_type == "exact" ):
                clauses.append("work_id = :work_id")
            elif ( match_type == "contains" ):
                clauses.append("work_id LIKE :work_id")
                field_dict["work_id"] = "%" + field_dict["work_id"] + "%"
        if ( "title" in field_dict ):
            if ( match_type == "exact" ):
                clauses.append("title = :title")
            elif ( match_type == "contains" ):
                clauses.append("title LIKE :title")
                field_dict["title"] = "%" + field_dict["title"] + "%"
        if ( "description" in field_dict ):
            if ( match_type == "exact" ):
                clauses.append("description = :description")
            elif ( match_type == "contains" ):
                clauses.append("description LIKE :description")
                field_dict["description"] = "%" + field_dict["description"] + "%"
        if ( "work_created_ts" in field_dict ):
            # TODO - figure out how to safely query ranges
            clauses.append("date(work_created_ts) = date(:work_created_ts")
        if ( "inserted_ts" in field_dict ):
            # TODO - figure out how to safely query ranges\
            clauses.append("date(inserted_ts) = date(:inserted_ts")
        retrieve_sql = ("""\
            SELECT
                work_id,
                title,
                description,
                datetime(work_created_ts) AS work_created,
                datetime(inserted_ts) AS inserted
            FROM """ + self._table_prefix + """works 
            WHERE """ + join_type.join(clauses)
        )
        retrieve_cur = self._db_conn.cursor()
        retrieve_cur.execute(retrieve_sql, field_dict)
        results = retrieve_cur.fetchone()
        return dict(results)