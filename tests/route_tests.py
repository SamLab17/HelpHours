import unittest
import sys
sys.path.append('../helphours')
sys.path.append('..')
from helphours import app


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
