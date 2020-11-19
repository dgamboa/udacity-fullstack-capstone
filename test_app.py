import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, actor_movies

# --------------------------------------------------------------------------- #
# Actor model test suite
# --------------------------------------------------------------------------- #
assistant_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlrN04xYXV3bWUyT0pTT3BmaG1qOSJ9.eyJpc3MiOiJodHRwczovL2thbmUtZmlsbXMtY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjQyOGQ1MWJkYTAwMDA3NWUwZmRlNyIsImF1ZCI6InJlc291cmNlcyIsImlhdCI6MTYwNTc1MzM5NCwiZXhwIjoxNjA1ODM5Nzk0LCJhenAiOiJMWm82V3ltckYxQkFnUERxODBpVWZENnhObWFzdzNHcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.oWw-zWRENdS9jMAjUUhI5XRVDrwjIDJVfoUAugdj0e-IKbGseMfCaKvZjCFPRqMhoEhRfh-oLgImeXjeo3J1xf2CvWuEDQhSK_L8nlOH23bNflLEHvKRkg7onTrWsG3FT0p0w6JoEw_mMiIglMsksAGG6L22AB9SBqEvbADozOY26VLQE8OENsn1P0qZK_yGlSwm_Gng2OXHxlS1G1mNSkpxwVBbYiTdleCEEB0C1EM_uAivReeSLshdlaJiKjiBs_1TX9VksBUyyKkipG5N-OMOCkYj4r-DDwuPXXopO15Eq2nV6qx2xFfzwkf07rNcaSbDYOseZ8lHBJLxUcVWaA'
director_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlrN04xYXV3bWUyT0pTT3BmaG1qOSJ9.eyJpc3MiOiJodHRwczovL2thbmUtZmlsbXMtY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjQyODM0MGJkNGMyMDA2OGY1Zjg3ZiIsImF1ZCI6InJlc291cmNlcyIsImlhdCI6MTYwNTc1MzQ0MiwiZXhwIjoxNjA1ODM5ODQyLCJhenAiOiJMWm82V3ltckYxQkFnUERxODBpVWZENnhObWFzdzNHcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.z5zqfHlxkuDVJar3L84rCbzquKPBrVeRY_o037GAacJ1zJf5lawfAxE-gJsj7KV0Kw3tvP76FF_wFYT23Lvb8kytcL-hJted6wg2NBAJz3ddWK6nOPZaqXCVy_lYG1MmLapbgzVhrFP5ngwNMo4FpwJ4RJpL1fKhCKXk06GcCTJdbvg9AFRWZ7D1EALS0k_d0dCq0AcGHcJKd36YSD-tshb4L5fMtWFpVaEaC138lMi8cDPhLzlocd04bwX5WjJRxp7C17CL3hQr00TYqDuWkx2a4zCWM-CtHIXETIHcSqJ_uTX5iHiBN0AD_OWD4DKo_jOvo1Y_LcL0_InjthGKDA'
producer_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlrN04xYXV3bWUyT0pTT3BmaG1qOSJ9.eyJpc3MiOiJodHRwczovL2thbmUtZmlsbXMtY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjJkMDE3NjYyNzVkMDA2ZTVhMjM3MSIsImF1ZCI6InJlc291cmNlcyIsImlhdCI6MTYwNTc1MzQ4OCwiZXhwIjoxNjA1ODM5ODg4LCJhenAiOiJMWm82V3ltckYxQkFnUERxODBpVWZENnhObWFzdzNHcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.BeH1I27evj8i97_3h5eIC9avUtKHh96MwTcCrNYGeR3gV5gcdKSiHzhAyzyHQM6W9IarY1gdjFYZDL65V7_6LvxM03xwDrAcZlU9YAki_LOaIaDnB9seJ8EwhGy42f37PyRcWFCxDa8LtS6Stum3cBGbKDhkI0T8dbawdJ-akEmHCQ7hww2jsg9H6e-pOfpAWe3Vbq-pIbcfj0qIQa-2lbhj8TFtUJWktdgJik2JSD6Nckqy5o3QFSJf6o3S0C91ROw38InoT1fUj-ko0qZebDd1AgpCiDL4YPXfiXp-IzPBXKAJ6Pi35KgvnNcB-WkgygqmFduvrgQKEpyr8LvkWg'


# --------------------------------------------------------------------------- #
# Actor model test suite
# --------------------------------------------------------------------------- #
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

        # Define tokens for tests
        if os.environ.get('ASSISTANT_TOKEN') is None:
            self.assistant_header = assistant_header
            self.director_header = director_header
            self.producer_header = producer_header
        else:
            self.assistant_header = os.environ.get('ASSISTANT_TOKEN')
            self.director_header = os.environ.get('DIRECTOR_TOKEN')
            self.producer_header = os.environ.get('PRODUCER_TOKEN')

    def tearDown(self):
        # Execute after each test
        pass

    # Test GET actors endpoint
    def test_get_all_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization': self.assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    # Test DELETE actors endpoint
    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/2',
    #                                 headers = {'Authorization':
    #                                            self.director_header})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['number_of_actors'])
    #     self.assertTrue(len(data['actors']))

    def test_422_if_actor_to_delete_does_not_exist(self):
        res = self.client().delete('actors/100',
                                   headers={'Authorization': self.director_header})
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

        res = self.client().post('/actors', json=new_actor,
                                 headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['number_of_actors'])

    def test_400_if_create_actor_fails_from_empty_form(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': self.director_header})
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

        res = self.client().post('/actors', json=bad_actor,
                                 headers={'Authorization': self.director_header})
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

        res = self.client().patch('/actors/2', json=updated_actor,
                                  headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 2)
        self.assertTrue(data['number_of_actors'])
        self.assertTrue(len(data['actors']))

    def test_422_if_update_actor_fails_from_empty_form(self):
        res = self.client().patch('/actors/2',
                                  headers={'Authorization': self.director_header})
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

        res = self.client().patch('/actors/2', json=another_bad_actor,
                                  headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# --------------------------------------------------------------------------- #
# Movie model test suite
# --------------------------------------------------------------------------- #
class MovieTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                         self.database_name)
        setup_db(self.app, self.database_path)

        # Bind the app to the appropriate context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        # Define tokens for tests
        if os.environ.get('ASSISTANT_TOKEN') is None:
            self.assistant_header = assistant_header
            self.director_header = director_header
            self.producer_header = producer_header
        else:
            self.assistant_header = os.environ.get('ASSISTANT_TOKEN')
            self.director_header = os.environ.get('DIRECTOR_TOKEN')
            self.producer_header = os.environ.get('PRODUCER_TOKEN')

    def tearDown(self):
        # Execute after each test
        pass

    # Test GET movies endpoint
    def test_get_all_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization': self.assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    # Test DELETE movies endpoint
    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/2',
    #                                headers={'Authorization': self.producer_header})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['number_of_movies'])
    #     self.assertTrue(len(data['movies']))

    def test_422_if_movie_to_delete_does_not_exist(self):
        res = self.client().delete('movies/100',
                                   headers={'Authorization': self.producer_header})
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

        res = self.client().post('/movies', json=new_movie,
                                 headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['number_of_movies'])

    def test_400_if_create_movie_fails_from_empty_form(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_if_create_actor_fails_from_bad_form(self):
        bad_movie = {
            'title': 'Gigli',
            'release': '!'
        }

        res = self.client().post('/movies', json=bad_movie,
                                 headers={'Authorization': self.producer_header})
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

        res = self.client().patch('/movies/2', json=updated_movie,
                                  headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 2)
        self.assertTrue(data['number_of_movies'])
        self.assertTrue(len(data['movies']))

    def test_422_if_update_movie_fails_from_empty_form(self):
        res = self.client().patch('/movies/2',
                                  headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_update_movie_fails_from_bad_form(self):
        another_bad_movie = {
            'title': 'Something Else',
            'release': '!'
        }

        res = self.client().patch('/movies/2', json=another_bad_movie,
                                  headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


if __name__ == "__main__":
    unittest.main()
