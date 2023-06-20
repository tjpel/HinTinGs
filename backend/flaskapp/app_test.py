from flaskapp import app
import unittest

class FlaskTestCase(unittest.TestCase):
    
        def test_query(self):
            tester = app.test_client(self)
            response = tester.get('/query', content_type='html/text')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'GET received')
    
        def test_documents(self):
            tester = app.test_client(self)
            response = tester.get('/documents', content_type='html/text')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'Hello, World!')

if __name__ == '__main__':
     unittest.main()