import os

from flask import (
    Flask,
    request,
    abort,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import (
    setup_db,
    Actor,
    Movie,
    actor_movies
)
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS to explicitly allow all origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

# -------------------------------------------------------------------------- #
# CORS Headers
# -------------------------------------------------------------------------- #
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

# ------------------------------------------------------------------------- #
# API Endpoints
# ------------------------------------------------------------------------- #
    # Index route for home page
    @app.route('/')
    def home():
        return jsonify({
            'welcome': 'Welcome to Kane Films, executive producers connecting actors and movies',
            'context': 'Capstone project for Udacity\'s Full Stack nanodegree',
            'author': 'Daniel Gamboa',
            'date': '2020-11-20'
        })

    # GET all actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = {actor.id: actor.name for actor in actors}

        if len(formatted_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': formatted_actors,
            'number_of_actors': len(Actor.query.all())
        })

    # DELETE an actor / actress
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = {actor.id: actor.name for actor in actors}

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': formatted_actors,
                'number_of_actors': len(Actor.query.all())
            })

        except BaseException as e:
            print(e)
            abort(422)

    # POST (or create) an actor / actress
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        try:
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = {actor.id: actor.name for actor in actors}

            return jsonify({
                'success': True,
                'created': actor.id,
                'actors': formatted_actors,
                'number_of_actors': len(Actor.query.all())
            })

        except BaseException as e:
            print(e)
            abort(422)

    # PATCH (or update) an actor / actress
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        try:
            body = request.get_json()

            actor = Actor.query.get(actor_id)
            new_name = body.get('name')
            new_age = body.get('age')
            new_gender = body.get('gender')

            if new_name:
                actor.name = new_name

            if new_age:
                actor.age = new_age

            if new_gender:
                actor.gender = new_gender

            actor.update()

            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = {actor.id: actor.name for actor in actors}

            return jsonify({
                'success': True,
                'updated': actor.id,
                'actors': formatted_actors,
                'number_of_actors': len(Actor.query.all())
            })

        except BaseException as e:
            print(e)
            abort(422)

    # GET all movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = {movie.id: movie.title for movie in movies}

        if len(formatted_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': formatted_movies,
            'number_of_movies': len(Movie.query.all())
        })

    # DELETE a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = {movie.id: movie.title for movie in movies}

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': formatted_movies,
                'number_of_movies': len(Movie.query.all())
            })

        except BaseException as e:
            print(e)
            abort(422)

    # POST (or create) a movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        new_title = body.get('title')
        new_release = body.get('release')

        try:
            movie = Movie(title=new_title, release=new_release)
            movie.insert()

            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = {movie.id: movie.title for movie in movies}

            return jsonify({
                'success': True,
                'created': movie.id,
                'movies': formatted_movies,
                'number_of_movies': len(Movie.query.all())
            })

        except BaseException as e:
            print(e)
            abort(422)

    # PATCH (or update) a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        try:
            body = request.get_json()

            movie = Movie.query.get(movie_id)
            new_title = body.get('title')
            new_release = body.get('release')

            if new_title:
                movie.title = new_title

            if new_release:
                movie.release = new_release

            movie.update()

            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = {movie.id: movie.title for movie in movies}

            return jsonify({
                'success': True,
                'updated': movie.id,
                'movies': formatted_movies,
                'number_of_movies': len(Movie.query.all())
            })

        except BaseException as e:
            print(e)
            abort(422)

# ------------------------------------------------------------------------- #
# Error Handlers
# ------------------------------------------------------------------------- #
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def authorization_error(e):
        return jsonify({
            'success': False,
            'error': e.status_code,
            'message': e.error['code']
        }), e.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
