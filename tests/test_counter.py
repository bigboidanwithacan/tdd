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
        """It should update a counter and increase its value by 1"""
        create_result = self.client.post('/counters/dan')
        self.assertEqual(create_result.status_code, 201)
        baseline_value = create_result.json['dan']
        update_result = self.client.put('/counters/dan')
        self.assertEqual(update_result.status_code, 200)
        updated_value = update_result.json['dan']
        self.assertEqual(updated_value, baseline_value + 1)
        
    def test_get_a_counter(self):
        """It should return the value of the counter"""
        create_result = self.client.post('/counters/alex')
        self.assertEqual(create_result.status_code, 201)
        get_result = self.client.get('/counters/alex')
        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.json['alex'], 0)