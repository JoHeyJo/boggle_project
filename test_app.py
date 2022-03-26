from unittest import TestCase

from app import app, games

from boggle import BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test.
        """
        self.client = app.test_client()
        app.config['TESTING'] = True

        test_board = BoggleGame(fill_letters=("B") + ("A") + ("T"))
        print(test_board)

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn("<title>Boggle</title>", html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            resp = client.post("/api/new-game")
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            isinstance(json_data["gameId"],str)
            isinstance(json_data["board"],list)
            self.assertIn(json_data["gameId"], games.keys())
            #self.assertIn({"gameId" : asdf, "board": asdf},games)
            #test to see if our html contains game id and games[id].board
            #self.asssertin(new game in games)
            # write a test for this route

    def test_scoring_words(self):
        #check for word

        with self.client as client:

            resp = client.post("/api/new-game")
            json_data = resp.get_json()

            gameId = json_data["gameId"]

            game = games[gameId]

            game.board = [
                ["C","A","T","H","P"], 
                ["O", "X", "X","K","R"], 
                ["X", "G", "X","O","A"], 
                ["B","C","E","B","T"], 
                ["E","L","T","E","B"]]

            resp = client.post("/api/score-word",json={"gameId":gameId, "word":'CAT'})
            json_data = resp.get_json()
            self.assertEqual("ok", json_data["result"])

            resp = client.post("/api/score-word",json={"gameId":gameId, "word":'HPK'})
            json_data = resp.get_json()
            self.assertEqual("not-word", json_data["result"])

            
            resp = client.post("/api/score-word",json={"gameId":gameId, "word":'ZZZ'})
            json_data = resp.get_json()
            self.assertEqual("not-on-board", json_data["result"])

