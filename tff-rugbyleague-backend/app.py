from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Timer
import logging
from state_machine import MatchStateMachine
from events.log_event import log_event

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class Player:
    def __init__(self, id, name, position, age, strength, pace, fitness, leadership, passing, shortKicking, longKicking, goalKicking, tackling, catching, sideStepping, offloading, instinct, discipline, interchange, team):
        self.id = id
        self.name = name
        self.position = position
        self.age = age
        self.strength = strength
        self.pace = pace
        self.fitness = fitness
        self.leadership = leadership
        self.passing = passing
        self.short_kicking = shortKicking
        self.long_kicking = longKicking
        self.goal_kicking = goalKicking
        self.tackling = tackling
        self.catching = catching
        self.side_stepping = sideStepping
        self.offloading = offloading
        self.instinct = instinct
        self.discipline = discipline
        self.interchange = interchange
        self.team = team
        self.fatigue = 0
        self.rating = 50

class Team:
    def __init__(self, team_data):
        self.name = team_data['name']
        self.primary_colour = team_data['primaryColour']
        self.secondary_colour = team_data['secondaryColour']
        self.players = []
        self.score = 0

class Match:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.commentary = []
        self.current_tackle_count = 1
        self.current_team_possession = 1
        self.current_seconds = 0
        self.current_half = 1
        self.current_position_x = 35  # 0 = Left Touchline, 35 = Centre, 70 = Right Touchline
        self.current_position_y = 60  # 0 = Team A In-Goal, 60 = Centre, 110 = Team B Try Line
        self.speed_ratio = 1
        self.state_machine = MatchStateMachine(self)  # Initialise the state machine

    def start_game(self):
        log_event(self, "The game begins!", 0, 5)
        self.state_machine.start()  # Start the state machine, beginning with the kickoff state
        self.state_machine.run()

# Global variables for team and match instances
team1 = None
team2 = None
match = None

@app.route('/start-game', methods=['POST'])
def start_game():
    global team1, team2, match
    data = request.json
    logging.info(data['team1'])

    # Initialise teams with names and colors
    team1 = Team(data['team1'])
    team2 = Team(data['team2'])

    # Add players to teams
    team1.players = [Player(**player, team=team1) for player in data['team1']['players']]
    team2.players = [Player(**player, team=team2) for player in data['team2']['players']]

    # Initialise the match and start it
    match = Match(team1, team2)
    match.start_game()

    return jsonify({"commentary": match.commentary})

@app.route('/pause-game', methods=['POST'])
def pause_game():
    if match:
        # Toggle the paused state using the state machine
        is_paused = match.state_machine.toggle_pause()
        return jsonify({"paused": is_paused})
    else:
        return jsonify({"error": "Match not started!"}), 400

@app.route('/get-match-state', methods=['GET'])
def get_match_state():
    if match:
        return jsonify({
            "paused": match.state_machine.paused,
            "team1_score": match.team1.score,
            "team2_score": match.team2.score,
            "team1_state": {p.id: {
                "name": p.name, 
                "fatigue": p.fatigue, 
                "rating": p.rating,
                "interchange": p.interchange
            } for p in match.team1.players},
            "team2_state": {p.id: {
                "name": p.name, 
                "fatigue": p.fatigue, 
                "rating": p.rating,
                "interchange": p.interchange
            } for p in match.team2.players},
            "commentary": match.commentary,
            "current_half": match.current_half,
            "current_seconds": match.current_seconds,
            "current_tackle_count": match.current_tackle_count,
            "current_team_possession": match.current_team_possession,
            "current_position_x": match.current_position_x,
            "current_position_y": match.current_position_y
        })
    else:
        return jsonify({"error": "Match not started!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
