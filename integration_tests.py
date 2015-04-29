
import unittest
from flask.ext.testing import TestCase
import core


class Tests(TestCase):
    render_templates = True
    run_gc_after_test = False

    def create_app(self):
        app = core.app
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def test_server_is_up_and_running(self):
        response = self.client.get('/')
        self.assertNotEqual(response, '')

    def test_root_route(self):
        self.client.get('/')
        self.assert_template_used('index.html')

    def test_online_user_count(self):
        response = self.client.get('/online')
        self.assertEquals(response.json, dict(result=0))

    def test_calculate_current(self):
        response = self.client.get('/calculate_current')
        self.assertNotEqual(response, 0)

if __name__ == '__main__':
    unittest.main()