import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie, actor_movies


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS to explicitly allow all origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    #--------------------------------------------------------------------------#
    # CORS Headers
    #--------------------------------------------------------------------------#
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    #--------------------------------------------------------------------------#
    # API Endpoints
    #--------------------------------------------------------------------------#

    # GET all actors
    @app.route('/actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = {actor.id: actor.name for actor in actors}

        if len(formatted_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': formatted_actors,
            'number_of_actors': len(Actor.query.all())
        })


    # GET all movies
    @app.route('/movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = {movie.id: movie.title for movie in movies}

        if len(formatted_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': formatted_movies,
            'number_of_movies': len(Movie.query.all())
        })


    #--------------------------------------------------------------------------#
    # Error Handlers
    #--------------------------------------------------------------------------#
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
