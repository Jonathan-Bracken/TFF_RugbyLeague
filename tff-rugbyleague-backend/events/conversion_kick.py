# events/conversion_kick.py

import random

def conversion_kick(match):
    from events.log_event import log_event
    
    scoring_team = match.team1 if match.current_team_possession == 1 else match.team2
    kicker = max(scoring_team.players, key=lambda p: p.goal_kicking)
    
    # Calculate the difficulty of the kick based on x position
    kick_difficulty_x = abs(match.current_position_x - 35) / 100  # Normalises difficulty between 0 and 1

    # Calculate the success probability considering kicker's skill and difficulty
    success_probability = kicker.goal_kicking / 100 * (1 - kick_difficulty_x)

    if random.random() < success_probability:
        scoring_team.score += 2
        log_event(match, f"{kicker.name} successfully converts the try.", 60, 3)
    else:
        log_event(match, f"{kicker.name} misses the conversion.", 60, 3)
    
    # Log the updated score
    log_event(match, f"Score update: {match.team1.name} {match.team1.score} - {match.team2.name} {match.team2.score}", 0, 3)
    match.current_team_possession = 1 if match.current_team_possession == 2 else 2

    if match.current_seconds >= 2400 and match.current_half == 1:
        return {"event": "half_time"}
    elif match.current_seconds >= 4800:
        return {"event": "full_time"}
    
    # Proceed to kickoff
    return {"event": "kick_off"}