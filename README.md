# Kane Films | Executive Producers

This is a simple application API for managing movie and actor records in a PostgreSQL database. I built it from scratch as the capstone project for [Udacity's](https://www.udacity.com/) [Full Stack nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

The primary objective of the project is to demonstrate proficiency with the full stack skills developed throughout the nanodegree - mainly, database build out, manipulation and interactions; API endpoint structuring, testing and error handling; authentication with third party systems, roles and permissions; testing with [Postman](https://www.postman.com/) and deployment with [Heroku](https://www.heroku.com).

The [Kane Films](https://kane-films-capstone.herokuapp.com/) application consists of a database that contains movie and actor records accessible via RESTful endpoints.  At this point the project doesn't have a browser-based frontend and requests are best sent and received via [Postman](https://www.postman.com/) or [curl](https://curl.haxx.se/download.html). The endpoints allow authenticated users to create, read, updated and delete movies and actors depending on their permission level. Authentication is handled via JWT tokens and managed through [Auth0](https://auth0.com/).

## Geting Started
###Pre-Requisites and Local Development
To get started you will need to have [Python3](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) and [pip](https://pypi.org/project/pip/) installed on your local environment. In order to keep dependencies separate and organized, you should set up a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### Dependencies
In the main project directory run:
```
pip install -r requirements.txt
```
This will install all of the required packages within the **requirements.txt** file.

Key dependencies include the following:

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [PostgreSQL](https://www.postgresql.org/) and [psycopg2](https://pypi.org/project/psycopg2/) to handle data persistence and database management.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) as the object relational mapping tools to interact with the database through [Python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

- [CORS](https://flask-cors.readthedocs.io/en/latest/) is a Flask extension to handle [Cross Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

#### Running the Server Locally

From within the main project directory activate the virtual environment and set the environment variables that will point the Flask server to the app by running:

```
export FLASK_APP=api.py
```

You should also considering configuring the server such that updates in your code are automatically reloaded into the running server. You can do this by running:

```
export FLASK_ENV=development
```

To activate the server, run:

```
flask run
```

#### Heroku API

In order to interact with the live application hosted on [Heroku](https://www.heroku.com), you can send [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) requests at:
[https://kane-films-capstone.herokuapp.com/](https://kane-films-capstone.herokuapp.com/)

You can send requests using [Postman](https://www.postman.com/) or [curl](https://curl.haxx.se/download.html). If you choose to use [Postman](https://www.postman.com/), you will find a [ready-made collection in the main project directory](https://github.com/dgamboa/udacity-fullstack-capstone/blob/master/kane-films.postman_collection.json).

## API Reference


### Error Handling


### Endpoints


## About the Stack


## Authors
Daniel Gamboa, Udacity Full Stack Nanodegree Student

## Acknowledgements
Thank you to the [Udacity](https://www.udacity.com/) team for developing the learning experience that culminated in my ability to build and deploy this capstone project from scratch.
