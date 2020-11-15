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


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
