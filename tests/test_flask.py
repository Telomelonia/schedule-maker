import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter Timeslots and Rooms', response.data)

    def test_submit(self):
        response = self.app.post('/submit', data={
            'timeslot': ['1,MONDAY,8,30,9,30', '2,MONDAY,9,30,10,30'],
            'room': ['1,Room A', '2,Room B'],
            'lesson': ['1,Math,Mr. Smith,1,1', '2,Science,Ms. Johnson,2,2']
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

if __name__ == '__main__':
    unittest.main()