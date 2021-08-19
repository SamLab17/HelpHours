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

    # should be same as main page
    def test_index_page(self):
        response = self.app.get('/index', follow_redirects=True)
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
    """
    def test_zoom_redirect(self):
        response = self.app.get('/zoom', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_schedule_redirect(self):
        response = self.app.get('/schedule', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    """
    def test_about_page(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # unauthorized routes by default
    def test_change_zoom_page(self):
        response = self.app.get('/change_zoom', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_admin_panel(self):
        response = self.app.get('/admin_panel', follow_redirects=True)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
