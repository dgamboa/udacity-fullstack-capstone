import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Actor, Movie, actor_movies


#------------------------------------------------------------------------------#
# Actor model test suite
#------------------------------------------------------------------------------#
class ActorTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Bind the app to the appropriate context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        # Execute after each test
        pass


    # Test GET actors endpoint
    def test_get_all_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    # Test DELETE actors endpoint
    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/2')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['number_of_actors'])
    #     self.assertTrue(len(data['actors']))

    def test_422_if_actor_to_delete_does_not_exist(self):
        res = self.client().delete('actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test POST actors endpoint
    def test_create_actor(self):
        new_actor = {
            'name': 'Michael J. Fox',
            'age': 59,
            'gender': 'M'
        }

        res = self.client().post('/actors', json = new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['number_of_actors'])

    def test_400_if_create_actor_fails_from_empty_form(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_if_create_actor_fails_from_bad_form(self):
        bad_actor = {
            'name': 'That Guy',
            'age': 'NaN',
            'gender': 'M'
        }

        res = self.client().post('/actors', json = bad_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test PATCH actors endpoint
    def test_update_actor(self):
        updated_actor = {
            'name': 'Feelix New',
            'age': 35,
            'gender': 'M'
        }

        res = self.client().patch('/actors/2', json = updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 2)
        self.assertTrue(data['number_of_actors'])
        self.assertTrue(len(data['actors']))

    def test_422_if_update_actor_fails_from_empty_form(self):
        res = self.client().patch('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_update_actor_fails_from_bad_form(self):
        another_bad_actor = {
            'name': 'Another Bad',
            'age': 'NaN',
            'gender': 'M'
        }

        res = self.client().patch('/actors/2', json = another_bad_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

#------------------------------------------------------------------------------#
# Movie model test suite
#------------------------------------------------------------------------------#
class MovieTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Bind the app to the appropriate context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        # Execute after each test
        pass


    # Test GET movies endpoint
    def test_get_all_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    # Test DELETE movies endpoint
    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/2')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['number_of_movies'])
    #     self.assertTrue(len(data['movies']))

    def test_422_if_movie_to_delete_does_not_exist(self):
        res = self.client().delete('movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test POST movies endpoint
    def test_create_movie(self):
        new_movie = {
            'title': 'Back to the Future',
            'release': '1985-07-03'
        }

        res = self.client().post('/movies', json = new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['number_of_movies'])

    def test_400_if_create_movie_fails_from_empty_form(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_if_create_actor_fails_from_bad_form(self):
        bad_movie = {
            'title': 'Gigli',
            'release': '!'
        }

        res = self.client().post('/movies', json = bad_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


if __name__ == "__main__":
    unittest.main()
