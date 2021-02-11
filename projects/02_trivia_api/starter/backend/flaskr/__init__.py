import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_items(request, items):
  page = request.args.get('page', 1 , type = int)
  start = (page-1)* QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in items]
  return questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def add_cors_headers(response):
    response.headers.add('Access-Control-Allow_Headers', 'Content_Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods = ['GET'])
  def retrive_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]
    result = {
      'success': True,
      'categories': formatted_categories
    }
    return jsonify(result)

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
  @app.route('/questions', methods = ['GET'])
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_items(request, questions)
    categories = Category.query.order_by(Category.id).all()
    categories_list = [category.type for category in categories]

    if len(current_questions) == 0:
      abort(404)

    result = {
      'success': True,
      'questions': current_questions,
      'total_questions':len(questions),
      'categories': categories_list,
      'current_category': None
    }
    return jsonify(result)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question == None:
      abort(404)
    question.delete()
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_items(request, questions)
    result = {
      'success':True,
      'questions':current_questions,
      'total_questions': len(questions),
    }
    return jsonify(result)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions/add', methods=['POST'])
  def create_question():
    body = request.get_json()
    question_text = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)
    question = Question(question=question_text, answer=answer, category=category, difficulty=difficulty)
    question.insert()
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_items(request, questions)
    categories = Category.query.order_by(Category.id).all()
    categories_list = [category.type for category in categories]

    return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(questions),
        'categories': categories_list,
        'current_category': None
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
  @app.route('/questions', methods = ['POST'])
  def search_question():
    body = request.get_json()
    search = body.get('searchTerm', None)
    if search:
      questions = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
      questions_list = [question.format() for question in questions]
      return jsonify({
        'success': True,
        'questions': questions_list,
        'total_questions': len(questions_list),
        'current_category': None
      })
      

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    questions_in_category = Question.query.filter(Question.category == str(category_id)).all()
    current_questions = paginate_items(request, questions_in_category)
    categories = Category.query.all()
    formatted_categories = [c.format() for c in categories]
    
    return jsonify({
      'success':True,
      'questions': current_questions,
      'total_questions': len(questions_in_category),
      'current_category':category_id
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

    
