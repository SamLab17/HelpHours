from .. import app
import unittest
import json


class JoinTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # See "open" token in config
        self.app.post('/open', data={'token': '312'})

    def tearDown(self):
        pass

    def test_simple_join(self):
        post_data = {
            'name': 'Alice',
            'email': 'example@example.com',
            'eid': 'al123',
            'desc': 'Testing problem description',
            'modality': 'virtual'
        }
        join_resp = self.app.post('/join', data=post_data, follow_redirects=True)
        self.assertEqual(join_resp.status_code, 200)
        queue_resp = self.app.get('/queue')
        queue = json.loads(next(queue_resp.response))['queue']
        self.assertIn({
            'name': 'Alice',
            'position': 0,
            'modality': 'virtual'
            }, queue)


if __name__ == '__main__':
    unittest.main()
