# events/penalty_kick.py

import random

def penalty_kick(match):
    from events.log_event import log_event

    if match.current_team_possession == 1:
            attacking_team = match.team1
            defending_team = match.team2
            kick_difficulty_y = abs(match.current_position_y - 100) / 200
    else:
            attacking_team = match.team2
            defending_team = match.team1
            kick_difficulty_y = abs(match.current_position_y - 20) / 200

    kicker = max(attacking_team.players, key=lambda p: p.goal_kicking)
    
    # Calculate the difficulty of the kick based on x position
    kick_difficulty_x = abs(match.current_position_x - 35) / 100  # Normalises difficulty between 0 and 1

    # Calculate the success probability considering kicker's skill and difficulty
    success_probability = kicker.goal_kicking / 100 * (1 - kick_difficulty_x) * (1 - kick_difficulty_y)

    match.current_team_possession = 1 if match.current_team_possession == 2 else 2

    if random.random() < success_probability:
        attacking_team.score += 2
        log_event(match, f"{kicker.name} successfully kicks the penalty.", 60, 5)
        # Log the updated score
        log_event(match, f"Score update: {match.team1.name} {match.team1.score} - {match.team2.name} {match.team2.score}", 0, 2)

        if match.current_seconds >= 2400 and match.current_half == 1:
            return { "event": "half_time" }
        elif match.current_seconds >= 4800:
            return { "event": "full_time" }
        
        return { "event": "kick_off" }
    else:
        match.current_team_possession = 1 if match.current_team_possession == 2 else 2
        log_event(match, f"{kicker.name} misses the penalty. {defending_team.name} will drop out.", 60, 5)
        return { "event": "drop_out" }