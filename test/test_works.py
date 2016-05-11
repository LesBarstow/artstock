from dal.sqlite3.db_maintenance import DbMaintenance
from works import Works
import os
import json # for debugging

class TestWorks(object):
    
    @classmethod
    def setup_class(self):
        # Fake a config file for testing. No need to actually read a config for now
        self.config = {
            # test database is in ${project_loc}/db/testartworks.s3db
            'dbpath': os.path.join(
                        os.path.dirname(
                            os.path.realpath(__file__)
                        ),
                        '..', 'db', 'testartworks.s3db'
                    ),
            # 'force' forces the db_maintenance init to delete an existing database
            'force': True
        }
        # Use DbMaintenance to delete and recreate a test database
        self.dbm = DbMaintenance(self.config)
        self.dbm.create_tables()
        
        # Set up the Works class, which we'll be testing.
        self.works = Works(self.config)
    
    @classmethod
    def teardown_class(self):
        self.dbm.db_finish()
    
    def TestWorkingCreate(self):
        create_args = {
            'work_id': 'AWTEST-001-01',
            'title': 'Testable Art',
            'description': 'Sample art for testing.'
        }
        assert self.works.create(create_args) is None

    def TestWorkingRetrieve(self):
        # When testing, always create a unique test row that doesn't depend
        # on previous test cases
        create_args = {
            'work_id': 'AWTEST-001-02',
            'title': 'Testable Art II',
            'description': 'More sample art for testing.'
        }
        self.works.create(create_args)
        
        retrieve_args = {
            'work_id': 'AWTEST-001-02'
        }
        # A little manipulation here. We don't know what timestamps will be
        # so retrieve results and delete them before comparing
        results = self.works.retrieve(retrieve_args)
        print(json.dumps(results))
        del results['work_created']
        del results['inserted']
        assert results == create_args