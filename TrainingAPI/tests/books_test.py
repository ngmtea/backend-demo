from main import app
import json
import unittest

test_book_id = "7ac1e6f7-7281-46dd-ba8a-9b7506310111"

class BooksTests(unittest.TestCase):
    """ Unit testcases for REST APIs """

    def test_1_get_all_books(self):
        request, response = app.test_client.get('/books')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_books'), 0)
        self.assertIsInstance(data.get('books'), list)

    def test_2_create_book(self):
        data_book = json.dumps({
            "title": "Test",
            "authors": [],
            "publisher": ""
        })
        headers = {
            'Authorization': ""
        }

        # Chua co Auth
        request, response = app.test_client.post('/books', data=data_book, headers=headers)
        self.assertEqual(response.status, 401)

        # Login
        data_user = json.dumps({
            "username": "admin29",
            "password": "123"
        })
        request, response = app.test_client.post('/users/login', data=data_user)
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.text)
        self.assertGreaterEqual(response_data.get('status'), 'Login success')
        token = response_data.get('account').get('jwt')
        self.assertIsInstance(token, str)

        headers['Authorization'] = token

        # Auth
        request, response = app.test_client.post('/books', data=data_book, headers=headers)
        response_data = json.loads(response.text)
        self.assertEqual(response.status, 200)
        self.assertGreaterEqual(response_data.get('status'), 'success')

    def test_3_put_book(self):
        data_book = json.dumps({
            "title": "Test1",
        })
        headers = {
            'Authorization': ""
        }

        # Chua co Auth
        request, response = app.test_client.put(f'/books/{test_book_id}', data=data_book, headers=headers)
        self.assertEqual(response.status, 401)

        # Login sai tai khoan
        data_user = json.dumps({
            "username": "admin",
            "password": "admin"
        })
        request, response = app.test_client.post('/users/login', data=data_user)
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.text)
        self.assertGreaterEqual(response_data.get('status'), 'Login success')
        token = response_data.get('account').get('jwt')
        self.assertIsInstance(token, str)

        headers['Authorization'] = token

        # Auth sai
        request, response = app.test_client.put(f'/books/{test_book_id}', data=data_book, headers=headers)
        self.assertEqual(response.status, 403)

        # Login dung tai khoan
        data_user = json.dumps({
            "username": "admin29",
            "password": "123"
        })
        request, response = app.test_client.post('/users/login', data=data_user)
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.text)
        self.assertGreaterEqual(response_data.get('status'), 'Login success')
        token = response_data.get('account').get('jwt')
        self.assertIsInstance(token, str)

        headers['Authorization'] = token

        # Auth dung
        request, response = app.test_client.put(f'/books/{test_book_id}', data=data_book, headers=headers)
        response_data = json.loads(response.text)
        self.assertEqual(response.status, 200)
        self.assertGreaterEqual(response_data.get('status'), 'data changed successfully')


    def test_4_delete_book(self):
        headers = {
            'Authorization': ""
        }

        # Chua co Auth
        request, response = app.test_client.delete(f'/books/{test_book_id}', headers=headers)
        self.assertEqual(response.status, 401)

        # Login sai tai khoan
        data_user = json.dumps({
            "username": "admin",
            "password": "admin"
        })
        request, response = app.test_client.post('/users/login', data=data_user)
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.text)
        self.assertGreaterEqual(response_data.get('status'), 'Login success')
        token = response_data.get('account').get('jwt')
        self.assertIsInstance(token, str)

        headers['Authorization'] = token

        # Auth sai
        request, response = app.test_client.delete(f'/books/{test_book_id}', headers=headers)
        self.assertEqual(response.status, 403)

        # Login dung tai khoan
        data_user = json.dumps({
            "username": "admin29",
            "password": "123"
        })
        request, response = app.test_client.post('/users/login', data=data_user)
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.text)
        self.assertGreaterEqual(response_data.get('status'), 'Login success')
        token = response_data.get('account').get('jwt')
        self.assertIsInstance(token, str)

        headers['Authorization'] = token

        # Auth dung
        request, response = app.test_client.delete(f'/books/{test_book_id}', headers=headers)
        response_data = json.loads(response.text)
        self.assertEqual(response.status, 200)
        self.assertGreaterEqual(response_data.get('status'), 'deleted successfully')


    def test_5_login(self):
        headers = {
            'Authorization': ""
        }

        #Sai ten dang nhap hoac mat khau
        data_user = json.dumps({
            "username": "admin",
            "password": "admin1"
        })
        request, response = app.test_client.post('/users/login', data=data_user)
        self.assertEqual(response.status, 400)

        #Login dung
        data_user = json.dumps({
            "username": "admin",
            "password": "admin"
        })
        request, response = app.test_client.post('/users/login', data=data_user)
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.text)
        self.assertGreaterEqual(response_data.get('status'), 'Login success')

    def test_6_register(self):
        #trung username
        data_user = json.dumps({
            "username": "admin",
            "password": "admin"
        })
        request, response = app.test_client.post('/users/register', data=data_user)
        self.assertEqual(response.status, 400)

        #dang ky thanh cong
        data_user = json.dumps({
            "username": "ad1",
            "password": "ad1"
        })
        request, response = app.test_client.post('/users/register', data=data_user)
        self.assertEqual(response.status, 200)
        response_data = json.loads(response.text)
        self.assertGreaterEqual(response_data.get('status'), 'register success')

    def test_7_get_all_user(self):
        request, response = app.test_client.get('/users')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_users'), 0)
        self.assertIsInstance(data.get('users'), list)


    # TODO: unittest for another apis


if __name__ == '__main__':
    unittest.main()
