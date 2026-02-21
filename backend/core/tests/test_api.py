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
