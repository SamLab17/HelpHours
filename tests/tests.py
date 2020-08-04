import unittest
import sys
sys.path.append('../helphours')
sys.path.append('..')
from student import Student
from helphours import app
#import labhoursapp.p
class TestStudent(unittest.TestCase):

    def test_name(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "")
        self.assertEqual("John Doe", x.name)

    def test_email(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "")
        self.assertEqual("john@gmail.com", x.email)

    def test_eid(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "")
        self.assertEqual("jd123", x.eid)

    def test_combined(self):
        x = Student("Jane Doe", "jane@gmail.com", "jd1234", "")
        self.assertEqual("Jane Doe", x.name)
        self.assertEqual("jane@gmail.com", x.email)
        self.assertEqual("jd1234", x.eid)

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_join_page(self):
        response = self.app.get('/join', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_page(self):
        response = self.app.get('/view', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_remove_page(self):
        response = self.app.get('/remove', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
