"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

class CounterTest(TestCase):
    """Counter tests"""
    
    
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    
    def setUp(self):
        self.client = app.test_client()
    
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)
        
    def test_update_a_counter(self):
        """Should successfully update a counter"""
        result = self.client.post('/counters/test')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result.json['test'], 0)
        toCompare = self.client.put('/counters/test')
        self.assertEqual(toCompare.status_code, status.HTTP_200_OK)
        self.assertEqual(result.json['test'] + 1, toCompare.json['test'])
        
    def test_get_a_counter(self):
        """It should return the value of the counter"""
        create_result = self.client.post('/counters/dan')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)
        get_result = self.client.get('/counters/dan')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)
        self.assertEqual(get_result.json['dan'], 0)
        
    def test_delete_a_counter(self):
        """It should delete a counter"""
        create_result = self.client.post('/counters/dan')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)
        delete_result = self.client.delete('/counters/dan')
        self.assertEqual(delete_result.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_a_non_existent_counter(self):
        """It should return a 404 for a non-existent counter"""
        result = self.client.delete('/counters/unknown')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_a_non_existent_counter(self):
        """It should return a 404 for a non-existent counter"""
        result = self.client.get('/counters/unknown')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_a_non_existent_counter(self):
        """It should return a 404 for a non-existent counter"""
        result = self.client.put('/counters/unknown')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)