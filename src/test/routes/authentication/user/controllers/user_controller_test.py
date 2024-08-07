import unittest
import pytest
import requests


class UserControllerTest(unittest.TestCase):

    def setUp(self):
        self.token = None
        self.url = 'http://localhost:8000/rest/api/v1/login'
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    @pytest.mark.asyncio
    def test_create_user_register_and_then_return_201(self):
        authorization = requests.post(self.url, json={'username': 'test', 'password': 'test'}, headers=self.headers)
        if authorization:
            self.token = authorization.json().get('authorization')
            self.headers.update({'Authorization': self.token})
        response = requests.post(url='http://localhost:8000/rest/api/v1/create_user',
                                 headers=self.headers, json={'name': 'New User',
                                                             'username': 'new_user',
                                                             'password': 'test123',
                                                             'password_confirmation': 'test123',
                                                             'email': 'test@test.com',
                                                             'is_active': True})
        self.assertEqual(response.json().get('status_code'), 201)
        self.assertEqual(response.json().get('detail'), 'User created successfully')

    @pytest.mark.asyncio
    def test_login_empty_username_should_return_400(self):
        response = requests.post(self.url, json={'username': '', 'password': 'test'}, headers=self.headers)
        self.assertEqual(response.json().get('status_code'), 400)
        self.assertEqual(response.json().get('detail'), 'Username is missing')

    @pytest.mark.asyncio
    def test_login_empty_password_should_return_400(self):
        response = requests.post(self.url, json={'username': 'test', 'password': ''}, headers=self.headers)
        self.assertEqual(response.json().get('status_code'), 400)
        self.assertEqual(response.json().get('detail'), 'Password is missing')

    @pytest.mark.asyncio
    def test_login_user_should_return_200_and_authorization_token(self):
        response = requests.post(self.url, json={'username': 'test', 'password': 'test'}, headers=self.headers)
        self.assertEqual(response.json().get('status_code'), 202)
        self.assertEqual(response.json().get('detail'), 'Accepted')

    @pytest.mark.asyncio
    def test_login_user_should_return_401_if_password_is_wrong(self):
        response = requests.post(self.url, json={'username': 'test', 'password': 'test123'}, headers=self.headers)
        self.assertEqual(response.json().get('status_code'), 401)
        self.assertEqual(response.json().get('detail'), 'Unauthorized')

    @pytest.mark.asyncio
    def test_login_user_should_return_404_if_user_is_not_found(self):
        response = requests.post(self.url, json={'username': 'test123', 'password': 'test'}, headers=self.headers)
        self.assertEqual(response.json().get('status_code'), 404)
        self.assertEqual(response.json().get('detail'), 'Not found')


if __name__ == '__main__':
    unittest.main()
