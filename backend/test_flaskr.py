import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Actor, Movie, actor_movies

#------------------------------------------------------------------------------#
# Actor model test suite
#------------------------------------------------------------------------------#
assistant_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlrN04xYXV3bWUyT0pTT3BmaG1qOSJ9.eyJpc3MiOiJodHRwczovL2thbmUtZmlsbXMtY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjQyOGQ1MWJkYTAwMDA3NWUwZmRlNyIsImF1ZCI6InJlc291cmNlcyIsImlhdCI6MTYwNTY0Mjc0MSwiZXhwIjoxNjA1NzI5MTQxLCJhenAiOiJMWm82V3ltckYxQkFnUERxODBpVWZENnhObWFzdzNHcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.xEi_0wWoX5jXmxUlvpsa4bKIbjqOKV5siKFPdaXDx1NjZlI0eim33JAPYJiSNbUBEUzwBpHq5lA6MtFh7nZi1bQkFFz6mpM2Yt8u6MTZMNPdqXmKtWGW2AC8KGyzdSkyfeT1hc9bpN-nfMoTs6ZR1zqF1bEI4jY5Wlego8EVLNyStIQoPZbJ2sicp5EiDzqyZQFKZohmOyXZ5yBhGJ0tBCY9Ejuq54pdc6E7tnjueGxCO0NckFSi_bMCERox8kQFtCh95hdZwcg4jVQ8cjA-IOtEoRhUX7FEa-QZVIjxKEwcL6MP1Y30SfbH8IvEjurVN2U99AmoY4XbtORjVCVFIA'
director_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlrN04xYXV3bWUyT0pTT3BmaG1qOSJ9.eyJpc3MiOiJodHRwczovL2thbmUtZmlsbXMtY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjQyODM0MGJkNGMyMDA2OGY1Zjg3ZiIsImF1ZCI6InJlc291cmNlcyIsImlhdCI6MTYwNTY0MjYzMSwiZXhwIjoxNjA1NzI5MDMxLCJhenAiOiJMWm82V3ltckYxQkFnUERxODBpVWZENnhObWFzdzNHcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.qhcuhLoKkmXWMYWqRX6nlCwbIdVhz3XUWjWuTMcH5vIuuQ4Zbiok6WQbe-z9urHsJH7T3Q95rVwyNH--oRsCGbiv2WX5Tg7OkuIICYGclj4UrY2VfZSx17STXGJ4begHKMZasSvcK3wyunhYJ_3mEy9ttcMrjDwxkaZiRJKoNDgfYMzVtPz5MqSQXfLOtTUblaCzwimCg_mR77HRyuCd8cD5GTJMNLh5ZLoNlAT6aEdZ3D8VbK2X5gc0Azxehem_1nxVZkNBKynp2x2Ti3q2GyxXVU9YWhtgaYFfZDpxTHriuGwv0ttc8bXg8QjZ3zZh7ao-KTf1DM3BO8Z1xDRFVw'
producer_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlrN04xYXV3bWUyT0pTT3BmaG1qOSJ9.eyJpc3MiOiJodHRwczovL2thbmUtZmlsbXMtY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjJkMDE3NjYyNzVkMDA2ZTVhMjM3MSIsImF1ZCI6InJlc291cmNlcyIsImlhdCI6MTYwNTY0MjcwOCwiZXhwIjoxNjA1NzI5MTA4LCJhenAiOiJMWm82V3ltckYxQkFnUERxODBpVWZENnhObWFzdzNHcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.HGGvqvu1fAL1VtrcRnWKKwqmN6gZqM3tCCy3re8RTtfFxiVOcZMwKhww74AdOVxuX7YAkGuUMh8sBUjy76RMp95gHhbnnzz1NlDo8ICqfhbYCqLg3-asZIsq3XSTjvo5RxeH25DCoSySUu0gfq2Iy3U-fdW-jwLxp58lko-iZtJT1PhC9www92YEs3If_WKnUklqNnyYuPvNkEhnN-LY31nI1f92_EMmdV1waCACNjYLlefhVFMAN-F2wJD0_Axg04ufwQd78txmnmqbm7J3Zt1GIZbg5IM-9DuYP12HA8mU-RNDAL3oQL2JeDLbHVdvqCANbpTlljyPooAti0Or3A'

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
        res = self.client().get('/actors', headers = {'Authorization': assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    # Test DELETE actors endpoint
    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/2', headers = {'Authorization': director_header})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['number_of_actors'])
    #     self.assertTrue(len(data['actors']))

    def test_422_if_actor_to_delete_does_not_exist(self):
        res = self.client().delete('actors/100', headers = {'Authorization': director_header})
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

        res = self.client().post('/actors', json = new_actor, headers = {'Authorization': director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['number_of_actors'])

    def test_400_if_create_actor_fails_from_empty_form(self):
        res = self.client().post('/actors', headers = {'Authorization': director_header})
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

        res = self.client().post('/actors', json = bad_actor, headers = {'Authorization': director_header})
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

        res = self.client().patch('/actors/2', json = updated_actor, headers = {'Authorization': director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 2)
        self.assertTrue(data['number_of_actors'])
        self.assertTrue(len(data['actors']))

    def test_422_if_update_actor_fails_from_empty_form(self):
        res = self.client().patch('/actors/2', headers = {'Authorization': director_header})
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

        res = self.client().patch('/actors/2', json = another_bad_actor, headers = {'Authorization': director_header})
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
        res = self.client().get('/movies', headers = {'Authorization': assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    # Test DELETE movies endpoint
    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/2', headers = {'Authorization': producer_header})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['number_of_movies'])
    #     self.assertTrue(len(data['movies']))

    def test_422_if_movie_to_delete_does_not_exist(self):
        res = self.client().delete('movies/100', headers = {'Authorization': producer_header})
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

        res = self.client().post('/movies', json = new_movie, headers = {'Authorization': producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['number_of_movies'])

    def test_400_if_create_movie_fails_from_empty_form(self):
        res = self.client().post('/movies', headers = {'Authorization': producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_if_create_actor_fails_from_bad_form(self):
        bad_movie = {
            'title': 'Gigli',
            'release': '!'
        }

        res = self.client().post('/movies', json = bad_movie, headers = {'Authorization': producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test PATCH movies endpoint
    def test_update_movie(self):
        updated_movie = {
            'title': 'Back to the Future Part II',
            'release': '1989-11-22'
        }

        res = self.client().patch('/movies/2', json = updated_movie, headers = {'Authorization': director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 2)
        self.assertTrue(data['number_of_movies'])
        self.assertTrue(len(data['movies']))

    def test_422_if_update_movie_fails_from_empty_form(self):
        res = self.client().patch('/movies/2', headers = {'Authorization': director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_update_movie_fails_from_bad_form(self):
        another_bad_movie = {
            'title': 'Something Else',
            'release': '!'
        }

        res = self.client().patch('/movies/2', json = another_bad_movie, headers = {'Authorization': director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


if __name__ == "__main__":
    unittest.main()
