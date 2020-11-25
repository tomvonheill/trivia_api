# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API endpoints

GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

### GET '/categories'
* * *
- **Description:** Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- **Request Arguments:** None
- **Returns:** An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```


### GET '/questions'
* * *
- **Description:** This will retrieve questions for you including the questions, page, total_question, categories, and current_category. It will return a 'page's' worth of questions which is equal to 10 questions.
- **Request Arguments:** A request argument is 'page' which should be an integer. If not given the page defaults to 1. 
- **Returns:**
```
{'questions': list of questions on given page],
'page': page requested,
'total_questions': total number of questions (not just on this page),
'categories': list of all categories,
'current_category': None}
```

### POST '/questions'
* * *
- **Description:** Post a new question, requires the questions, answer, category, and difficulty score
- **Request Arguments:** None
- **Post Arguments:**
```
{'question': text for what question to ask (str),
'answer' : the answer to the question (str),
'category': category of the question (int),
'difficulty': difficulty of the question (1-5) (int)
}
```
- **Returns:** 
	- **On Success**: will return a dictionary with the id of the new question, and the success being true {'question_added': id, 'success': True}
	- **On Success**: aborts 422 with a message.

### DELETE '/questions/<<int:question_id>>'
* * *
- **Description:** allows you to delete a specific question supplying a integer for the question id you want to delete
- **Request Arguments:**
- **Returns:**
	- **On success**: returns a dictionary with the id of the question deleted and success of True {'question_id_delted': question_id, 'success': True}
	- **On Failure** sborts 404 with a message

### POST '/questions/search'
* * *
- **Description:** case insensitive search for a question using a searchterm.
- **Request Arguments:** A request argument is 'page' which should be an integer. If not given the page defaults to 1. 
- **Post Arguments:**
```
{
'searchTerm': substring of question we are looking for.
}
```
- **Returns:** 
	- **On Success**: will return a dictionary with question, page, total questions, categories, and current category.
 ```
{'questions': list of questions on given page that match the search term,
 'page': page requested,
 'total_questions': total number of questions (not just on this page),
 'categories': list of all categories,
 'current_category': None}
```

### GET '/categories/<<int:category_id>>/questions'
* * *
- **Description:** gets teh questions for a given category (int:category_id) and returns a the page specified by the request arguments. 10 questions per page, will default to page 1 if no arguments are given.
- **Request Arguments:** A request argument is 'page' which should be an integer. If not given the page defaults to 1. 
- **Returns**
	- **On Success**: will return a dictionary with question, page, total questions, categories, and current category.
 ```
{'questions': list of questions on given page that match the search term,
 'page': page requested,
 'total_questions': total number of questions (not just on this page),
 'categories': list of all categories,
 'current_category': category specified by category_id}
```


### POST '/quizzes'
* * *
- **Description:** retrieves a random question for a given quiz category that is not one of the questions played before. Quiz category and questions played must be sent from client, the server does not keep track of the client's quiz progress.
- **Request Arguments:** None
- **Post Arguments:**  Post takes a dictionary with 'previous_questions' and 'quiz_category' as keys. Quiz category further has a interior dictionary that contains the key 'id' which is for determining the quiz category. 
- example: {'previous_questions': [19, 15, 9], 'quiz_category': {'id': 1, 'type': 'click'}} In this example we see taht the previous questions with ids 19, 15, 9 were played before and cannot show up. Also we see the 'id' of the quiz is 1 which will make sure we are returning a random question of category 1.
- **Returns:** 
	- **On Success**: will return a random question in the category that is not one of the previous_questions
 ```
{'question': 'question sample string?',
 'answer': 'answer to question retrieved',
 'category': category int,
 'difficulty': difficulty int between 0 and 5
 }
 ```
 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
