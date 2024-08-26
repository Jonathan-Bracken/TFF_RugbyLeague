# events/turnover.py

import random

def turnover(match):
    from events.log_event import log_event

    # Determine the new team in possession
    if match.current_team_possession == 1:
        match.current_team_possession = 2
        new_team = match.team2
    else:
        match.current_team_possession = 1
        new_team = match.team1
    
    log_event(match, f"Turnover. {new_team.name} will play the ball.", 10, 5)

    if match.current_seconds >= 2400 and match.current_half == 1:
        return {"event": "half_time"}
    elif match.current_seconds >= 4800:
        return {"event": "full_time"}
    
    match.current_tackle_count = 1
    
    return {"event": "dummy_half", "ball_player": random.choice(new_team.players)}