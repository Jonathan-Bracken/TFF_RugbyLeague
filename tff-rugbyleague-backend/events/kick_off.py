# events/kickoff.py

import random
from events.log_event import log_event

def kick_off(match):
    kicking_team = match.team1 if match.current_team_possession == 1 else match.team2
    direction = 1 if match.current_team_possession == 1 else -1
    match.current_position_x = 35
    match.current_position_y = 60
    # Kicker should be the most skilled long kicker in the team
    kicker = max(
        [p for p in kicking_team.players if not p.interchange], 
        key=lambda p: p.long_kicking,
        default=None 
    )
    log_event(match, f"{kicker.name} will kick off for {kicking_team.name}.", 0, 5)    

    # Perfect kickoff is approximately 50 metres
    base_distance = 50

    # A kick could be up to 40 metres short or 20 metres too long
    random_factor = random.uniform(-40, 20)

    # The kick length varies based on the long kicking ability
    skill_adjustment = kicker.long_kicking / 100
    kick_distance = base_distance + ( random_factor * (random.uniform(1, 1.2) - skill_adjustment))

    # Ensure the kick does not travel backwards
    kick_distance = max(kick_distance, 10)

    match.current_position_x = random.uniform(0, 70)
    match.current_position_y += (direction * kick_distance)

    # If the kick is more than 60 metres, it is out on the full and the opposition receive a penalty.
    # Otherwise, the opposition should attempt a catch.
    if match.current_position_y < 0 or match.current_position_y > 120:
        log_event(
            match, f"{kicker.name} kicks out on the full. Penalty to the opposition.", 5, 5
        )
        match.current_position_x = 35
        match.current_position_y = 60
        match.current_team_possession = 1 if match.current_team_possession == 2 else 2
        return {"event": "out_on_full"}
    else:
        log_event(match, f"{kicker.name} kicks off.", 5, 5)
        return {"event": "kicked_off", "kicker": kicker, "kick_type": "kick off", "kick_distance": kick_distance}
