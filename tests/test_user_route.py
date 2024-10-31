import unittest
from app import create_app, db
from models import User

class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_user(self):
        response = self.client.post('/api/users/', json={'username': 'testuser', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('testuser', response.get_data(as_text=True))

    def test_get_user(self):
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
        
        response = self.client.get(f'/api/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'testuser')

    def test_update_user(self):
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
        
        response = self.client.put(f'/api/users/{user.id}', json={'username': 'updateduser', 'email': 'updated@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'updateduser')

    def test_get_user_not_found(self):
        response = self.client.get('/api/users/999')
        self.assertEqual(response.status_code, 404)

    def test_update_user_not_found(self):
        response = self.client.put('/api/users/999', json={'username': 'updateduser', 'email': 'updated@example.com'})
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()