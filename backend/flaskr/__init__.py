import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  #this is the appliction factory
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  def page_lower_and_upper_bound(page):
      lower_bound = (page-1)*10
      upper_bound = lower_bound+10
      return lower_bound, upper_bound

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods = ['GET'])
  def get_categories():
    return jsonify({category.id : category.type for category in db.session.query(Category).all()})

  @app.route("/", methods = ['GET'])
  def homepage():
    return jsonify({
        'success': True
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.errorhandler(404)
  def questions_not_found(error):
    return jsonify({
      'success' : False,
      'error' : 404,
      'message' : 'No questions can be found'
    }, 404)
  
  @app.errorhandler(404)
  def question_not_found(error):
    return jsonify({
      'success' : False,
      'error' : 404,
      'message' : 'That question cannot be found'
    }, 404)
  
  @app.errorhandler(422)
  def uprocessable_request(error):
    return jsonify({
      'success' : False,
      'error' : 422,
      'message' : 'Unprocessable request'
    }, 422)

  @app.route('/questions', methods = ['GET'])
  def get_questions():
    page = int(request.args.get('page',1))
    lower_bound, upper_bound = page_lower_and_upper_bound(page)
    questions = db.session.query(Question).all()
    if not questions:
      questions_not_found()
    return jsonify({
    'questions': [question.format() for question in questions[lower_bound:upper_bound]],
    'page': page,
    'total_questions': len(questions),
    'categories': [category.type for category in db.session.query(Category).all()],
    'current_category': None,
    })




  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    try:
      question = db.session.query(Question).get(question_id)
      if not question:
        question_not_found()

      question.delete()
      db.session.commit()
      return jsonify({
      'question_id_deleted': question_id,
      'success':True,
    })

    except:
      uprocessable_request()

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods = ['POST'])
  def post_question():
    try:
      new_question = Question(**request.json)
      db.session.add(new_question)
      db.session.commit()
      return jsonify({
      'question_added': new_question.format(),
      'success':True,
    })

    except:
      db.session.rollback()
      abort(422)
    finally:
      db.session.close()
    return jsonify({
      'question_added': None,
      'success':False,
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods = ['POST'])
  def search_questions():
    try:
      page = int(request.args.get('page',1))
      if page:
        lower_bound, upper_bound = page_lower_and_upper_bound(page)
        search_term = request.json.get('searchTerm')
        questions = db.session.query(Question).filter(func.lower(Question.question).contains(func.lower(search_term))).all()
        if not questions:
          return questions_not_found()

      return jsonify({
      'questions': [question.format() for question in questions[lower_bound:upper_bound]],
      'page': page,
      'total_questions': len(questions),
      'categories': [category.type for category in db.session.query(Category).all()],
      'current_category': None,
      })
    except:
      uprocessable_request()

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
  def get_questions_by_category(category_id):
    page = int(request.args.get('page',1))
    lower_bound, upper_bound = page_lower_and_upper_bound(page)
    category_name = db.session.query(Category).get(category_id+1).type
    questions = db.session.query(Question).filter(Question.category == category_id+1).all()
    return jsonify({
    'questions': [question.format() for question in questions],
    'page': page,
    'total_questions': len(questions),
    'categories': [category.type for category in db.session.query(Category).all()],
    'current_category': category_name,
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    