from django.test import TestCase


class APITestCase(TestCase):
    def test_hello_endpoint(self):
        response = self.client.get('/api/hello')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('message', payload)
        self.assertIn('server_time', payload)
        self.assertIn('version', payload)

    def test_health_endpoint(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_signup_and_auth_me(self):
        response = self.client.post(
            '/api/auth/signup',
            data={'username': 'master1', 'password': 'pass1234', 'isMaster': True},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['user']['username'], 'master1')
        self.assertTrue(payload['user']['isMaster'])

        me_response = self.client.get('/api/auth/me')
        self.assertEqual(me_response.status_code, 200)
        self.assertTrue(me_response.json()['isAuthenticated'])

    def test_login_logout_flow(self):
        self.client.post(
            '/api/auth/signup',
            data={'username': 'player1', 'password': 'pass1234', 'isMaster': False},
            content_type='application/json',
        )
        self.client.post('/api/auth/logout', data={}, content_type='application/json')

        login_response = self.client.post(
            '/api/auth/login',
            data={'username': 'player1', 'password': 'pass1234'},
            content_type='application/json',
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertFalse(login_response.json()['user']['isMaster'])

        logout_response = self.client.post('/api/auth/logout', data={}, content_type='application/json')
        self.assertEqual(logout_response.status_code, 200)
        self.assertFalse(logout_response.json()['user']['isAuthenticated'])
