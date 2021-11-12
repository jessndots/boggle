from boggle import Boggle
from flask import Flask, request, render_template, jsonify, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret" 

debug=DebugToolbarExtension(app) # rest of file continues

boggle_game = Boggle()

@app.route('/')
def show_board(): 
    """Show boggle board"""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)


@app.route('/check-word')
def check_word(): 
    """Check if word is in dictionary and on board"""
    guess = request.args['guess']
    board = session['board']
    response = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': response})

@app.route('/post-score', methods=['POST'])
def post_score():
    """check if score broke record"""
    # request.get_json(force=True)
    game_score = request.json['score']
    high_score = session.get('high_score', 0)

    session['high_score'] = max(game_score, high_score)

    return jsonify(brokeRecord = game_score > high_score)
