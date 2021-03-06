import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category

load_dotenv()

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = os.environ.get("SQLALCHEMY_DATABASE_URI_BASE") + self.database_name
        setup_db(self.app, self.database_path)
        self.quiz_category = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginate(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)        
    
    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 6)

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
    
    def test_404_paginate_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')
    
    def test_delete_question(self):
        test_question = Question(question = 'test_delete', answer = 'test_delete_answer', category= 2, difficulty= 2)
        test_question.insert()
        test_question_id = test_question.id
        self.assertTrue(test_question_id)
        res = self.client().delete('/questions/{}'.format(str(test_question_id)))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(Question.query.filter(Question.id == test_question_id).one_or_none(), None)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_delete_question(self):
        questions = Question.query.all()
        question_ids = [question.id for question in questions]
        test_question_id = max(question_ids) + 1
        res = self.client().delete('/questions/{}'.format(str(test_question_id)))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'], 'Resource not found')
    
    def test_add_question(self):
        total_questions = Question.query.count()
        res = self.client().post('/questions/add', json = {
            'question': 'This is for test',
            'answer': 'Ok',
            'difficulty': 2,
            'category': 2
        })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(Question.query.count(), total_questions + 1)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
    
    def test_search_question(self):
        res = self.client().post('/questions', json = {'searchTerm': 'what'})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_retrieve_by_category(self):
        current_category = 2
        res = self.client().get('/categories/{}/questions'.format(str(current_category)))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], current_category)

    def test_404_retrieve_by_category(self):
        current_category = 20
        res = self.client().get('/categories/{}/questions'.format(str(current_category)))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json=self.quiz_category)
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
