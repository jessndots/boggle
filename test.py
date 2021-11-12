from unittest import TestCase
from app import app
from flask import session, jsonify, request
from boggle import Boggle
import pdb


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_show_board(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Scored words:</h3>', html)

    def test_valid_word(self):
        with app.test_client() as client: 
            with client.session_transaction() as sess:
                    sess['board'] = [['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S']]
            resp = client.get('/check-word?guess=guess')
            data = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('"result": "ok"', data)

    def test_invalid_word(self):
        with app.test_client() as client: 
            with client.session_transaction() as sess:
                    sess['board'] = [['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S']]
            resp = client.get('/check-word?guess=guest')
            data = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('"result": "not-on-board"', data)

    def test_non_english_word(self):
        with app.test_client() as client: 
            with client.session_transaction() as sess:
                    sess['board'] = [['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S'], ['G', 'U', 'E', 'S', 'S']]
            resp = client.get('/check-word?guess=fjkdal')
            data = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('"result": "not-word"', data)

    # def test_post_score(self):
    #     with app.test_client() as client:
    #         with client.session_transaction() as sess:
    #             sess['high_score'] = 85
    #         resp = client.post('/post-score', jsonify(data={'score': '100'}))
    #         resp_data = resp.get_data(as_text=True)
    #         self.assertIn('True', resp_data)
    #         self.assertEqual(resp.status_code, 200)


            




