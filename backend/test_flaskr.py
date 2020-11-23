import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    '''
    TO RUN Tests
    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py
    '''

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:yellow@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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

    #======= get_categories tests==========
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        category_information = {
            '1' : 'Science',
            '2': 'Art',
            '3': 'Geography',
            '4': 'History',
            '5': 'Entertainment',
            '6': 'Sports'
        }
        self.assertEqual(data, category_information)
    
    #========get_questions tests============
    def test_get_questions_sucess(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        categories = ['Science','Art','Geography','History','Entertainment','Sports']

        self.assertEqual(data['page'],1)
        self.assertEqual(data['categories'],categories)
        self.assertTrue(len(data['questions'])>0)
        self.assertIsNone(data['current_category'])
    
    def test_get_questions_unreachable_page(self):
        res = self.client().get('/questions?page=66')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Page 66 is out of range. No questions found.')
    
    #==========delete_question tests===========

    def test_succesfully_delete_question(self):
        res = self.client().delete('/questions/18')
        data = json.loads(res.data)
        self.assertEqual(data['question_id_deleted'], 18)
        self.assertTrue(data['success'])
        self.assertIsNone(db.session.query(Question).get(18))
    
    def test_unsuccesful_delete_of_missing_question(self):
        res = self.client().delete('/questions/18')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Question id 18 not found. Delete failed.')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()