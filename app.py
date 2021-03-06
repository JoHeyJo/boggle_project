from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    return jsonify({"gameId": game_id, "board": games[game_id].board})


@app.post("/api/score-word")
def score_word():
    """checks if word is legal 

    """
    
    response = request.json
    breakpoint()
    current_gameId = response["gameId"]
    current_board = games[current_gameId]
    
    isWordOnBoard = current_board.check_word_on_board(response['word'])
    isWordInList =  current_board.is_word_in_word_list(response['word'])
    #user is sending json
    if isWordInList and isWordOnBoard:
        return jsonify({"result": "ok"})

    if not isWordInList:
        return jsonify({"result": "not-word"})

    if not isWordOnBoard:
        return jsonify({"result": "not-on-board"})