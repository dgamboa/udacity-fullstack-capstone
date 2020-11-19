# Kane Films | Executive Producers
This is a simple application API for managing movie and actor records in a PostgreSQL database. I built it from scratch as the capstone project for [Udacity's](https://www.udacity.com/) [Full Stack nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

The primary objective of the project is to demonstrate proficiency with the full stack skills developed throughout the nanodegree - mainly, database build out, manipulation and interactions; API endpoint structuring, testing and error handling; authentication with third party systems, roles and permissions; testing with [Postman](https://www.postman.com/) and deployment with [Heroku](https://www.heroku.com).

The [Kane Films](https://kane-films-capstone.herokuapp.com/) application consists of a database that contains movie and actor records accessible via RESTful endpoints.  At this point the project doesn't have a browser-based frontend and requests are best sent and received via [Postman](https://www.postman.com/) or [curl](https://curl.haxx.se/download.html). The endpoints allow authenticated users to create, read, updated and delete movies and actors depending on their permission level. Authentication is handled via JWT tokens and managed through [Auth0](https://auth0.com/).

## Getting Started

### Pre-Requisites and Local Development
To get started you will need to have [Python3](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) and [pip](https://pypi.org/project/pip/) installed on your local environment. In order to keep dependencies separate and organized, you should set up a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### Dependencies
In the main project directory run:
```
pip install -r requirements.txt
```
This will install all of the required packages within the **requirements.txt** file. Key dependencies include the following:

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [PostgreSQL](https://www.postgresql.org/) and [psycopg2](https://pypi.org/project/psycopg2/) to handle data persistence and database management.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) as the object relational mapping tools to interact with the database through [Python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

- [CORS](https://flask-cors.readthedocs.io/en/latest/) is a Flask extension to handle [Cross Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

- [jose](https://python-jose.readthedocs.io/en/latest/) is JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Auth0](https://auth0.com/) to manage authentication and permissions.

#### Running the Server Locally
From within the main project directory activate the virtual environment and set the environment variables by running the bash script **setup.bash** as follows:

```
source setup.sh
```

To activate the server, run:

```
flask run
```

#### Test Suite
The main directory also contains a simple test suite for successful behavior of the API's endpoints and common errors. The tests file is located at [test_app.py](https://github.com/dgamboa/udacity-fullstack-capstone/blob/master/test_app.py). Note that you will have to generate new tokens and replace them in the constants at the top of the test file in order for the tests to run properly.

## API Reference

### Heroku-Based API
In order to interact with the live application hosted on [Heroku](https://www.heroku.com), you can send [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) requests to
[https://kane-films-capstone.herokuapp.com/](https://kane-films-capstone.herokuapp.com/)

You can send these requests using [Postman](https://www.postman.com/) or [curl](https://curl.haxx.se/download.html). If you choose to use [Postman](https://www.postman.com/), you will find a ready-made collection in the file named [kane-films.postman_collection](https://github.com/dgamboa/udacity-fullstack-capstone/blob/master/kane-films.postman_collection.json) located in the main project directory.

#### Setting Up Authentication
In order to utilize the API, you will need to sign up as a user. Please visit the link below and sign up with your preferred email and password.

[Sign Up!](https://kane-films-capstone.us.auth0.com/authorize?audience=resources&response_type=token&client_id=LZo6WymrF1BAgPDq80iUfD6xNmasw3Gq&redirect_uri=https://kane-films-capstone.herokuapp.com/)

After signing up you will be redirected to app's the [home page](https://kane-films-capstone.herokuapp.com/).

### Roles & Permissions
There are three user roles in the API:
- Assistants: permissions include `get:actors` and `get:movies`
- Directors: all of the Assistants' permissions as well as `post:actors`, `delete:actors`, `patch:actors` and `patch:movies`
- Producers: all of the Directors' permissions as well as `post:movies` and `delete:movies`

### Error Handling
If a request fails, the error object will include the following parameters in JSON format:
```
{
  'success': False,
  'error': 400,
  'message': 'bad request'
}
```
Other errors handled by the API include:
- 401: Unauthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error

### Endpoints
#### GET /actors
Returns a list of actors in the database organized by actor id as a dictionary stored in the *actors* variable. It also returns the total number of actors in the *number_of_actors* variable along with a *success* variable.
```
{
    "actors": {
        "1": "Oprah Winfrey",
        "2": "Summer Joy",
        "3": "Francine Mary",
        "4": "Allison Frost",
        "5": "Billy Rise",
        "6": "Will Trave"
    },
    "number_of_actors": 6,
    "success": true
}
```

#### GET /movies
Returns a list of movies in the database organized by movie id as a dictionary stored in the *movies* variable. It also returns the total number of movies in the *number_of_movies* variable along with a *success* variable.
```
{
    "movies": {
        "1": "Back to the Future Part II",
        "2": "Once A Starter",
        "3": "The Other End",
        "4": "A Cold Summer",
        "5": "A Turn Too Many",
        "6": "Flight Up"
    },
    "number_of_movies": 6,
    "success": true
}
```

#### POST /actors
Creates a new actor record and returns its actor id in the *created* variable and a list of actors in the database organized by actor id as a dictionary stored in the *actors* variable. It also returns the total number of actors in the *number_of_actors* variable along with a *success* variable.
```
{
    "actors": {
        "1": "Oprah Winfrey",
        "2": "Summer Joy",
        "3": "Francine Mary",
        "4": "Allison Frost",
        "5": "Billy Rise",
        "6": "Will Trave",
        "7": "Michael J. Fox"
    },
    "created": 7,
    "number_of_actors": 7,
    "success": true
}
```

#### POST /movies
Creates a new movie record and returns its movie id in the *created* variable and a list of movies in the database organized by movie id as a dictionary stored in the *movies* variable. It also returns the total number of movies in the *number_of_movies* variable along with a *success* variable.
```
{
    "created": 7,
    "movies": {
      "1": "Back to the Future Part II",
      "2": "Once A Starter",
      "3": "The Other End",
      "4": "A Cold Summer",
      "5": "A Turn Too Many",
      "6": "Flight Up",
      "7": "Back to the Future"
    },
    "number_of_movies": 7,
    "success": true
}
```

#### DELETE /actors/{actor_id}
Deletes the actor record specified by the *actor_id* parameter in the URL and returns the *actors*, *number_of_actors*, *success* and the *actor_id* variables.
```
{
    "actors": {
        "1": "Oprah Winfrey",
        "2": "Summer Joy",
        "3": "Francine Mary",
        "4": "Allison Frost",
        "6": "Will Trave",
        "7": "Michael J. Fox"
    },
    "deleted": 5,
    "number_of_actors": 6,
    "success": true
}
```

#### DELETE /movies/{movie_id}
Deletes the movie record specified by the *movie_id* parameter in the URL and returns the *movies*, *number_of_movies*, *success* and the *movie_id* variables.
```
{
    "deleted": 5,
    "movies": {
      "1": "Back to the Future Part II",
      "2": "Once A Starter",
      "3": "The Other End",
      "4": "A Cold Summer",
      "6": "Flight Up",
      "7": "Back to the Future"
    },
    "number_of_movies": 6,
    "success": true
}
```

#### PATCH /actors/{actor_id}
Updates the actor record specified by the *actor_id* parameter in the URL and returns the *actors*, *number_of_actors*, *success* and the *actor_id* variables.
```
{
    "actors": {
        "1": "Oprah Winfrey",
        "2": "Summer Joy",
        "3": "Francine Keller",
        "4": "Allison Frost",
        "6": "Will Trave",
        "7": "Michael J. Fox"
    },
    "updated": 3,
    "number_of_actors": 6,
    "success": true
}
```

#### PATCH /movies/{movie_id}
Updates the movie record specified by the *movie_id* parameter in the URL and returns the *movies*, *number_of_movies*, *success* and the *movie_id* variables.
```
{
    "updated": 4,
    "movies": {
      "1": "Back to the Future Part II",
      "2": "Once A Starter",
      "3": "The Other End",
      "4": "A Warm Summer",
      "6": "Flight Up",
      "7": "Back to the Future"
    },
    "number_of_movies": 6,
    "success": true
}
```

## Authors
[Daniel Gamboa](https://www.linkedin.com/in/dnlgmb/), Udacity Full Stack Nanodegree Student

## Acknowledgements
Thank you to the [Udacity](https://www.udacity.com/) team for developing the learning experience that culminated in my ability to build and deploy this capstone project from scratch.
