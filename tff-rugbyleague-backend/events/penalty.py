# events/penalty.py
import random

def penalty(self):
    from events.log_event import log_event

    team = self.team1 if self.current_team_possession == 1 else self.team2
    current_half = 1 if self.current_seconds <= 2400 else 2
    minutes_left = ( 2400 - self.current_seconds ) if current_half == 2 else ( 4800 - self.current_seconds )

    if self.current_team_possession == 1:
            distance_from_line = 110 - self.current_position_y
            current_score_difference = self.team1.score - self.team2.score
    else:
            distance_from_line = self.current_position_y - 10
            current_score_difference = self.team2.score - self.team1.score

    kick_goal = False
    
    if distance_from_line < 40:
        if current_score_difference >= -6 and minutes_left < 1 and current_half == 1:
                kick_goal = True
        if current_score_difference >= -2 and minutes_left < 1 and current_half == 2:
                kick_goal = True
        if current_score_difference >= -2 and current_score_difference <= 30 and random.random() < 0.5:
                kick_goal = True

    if (kick_goal == True):
        log_event(self, f"{team.name} will attempt to kick a penalty goal.", 0, 3)
        return {"event": "penalty_kick"}
    else:
        log_event(self, f"{team.name} will kick for touch.", 0, 3)
        return {"event": "kick_to_touch"}