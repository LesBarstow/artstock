
# import works

from builtins import classmethod

class TestWorks:
    
    @classmethod
    def setup_class(cls):
        pass
    
    @classmethod
    def teardown_class(cls):
        pass
    
    def test_01_create_out_of_range(self):
        assert 1==1
    
    def test_02_create_bogus(self):
        assert 1==0
    
