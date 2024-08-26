# events/drop_out.py

import random

def drop_out(match):
    from events.log_event import log_event

    if match.current_team_possession == 1:
        kicking_team = match.team1
        direction = 1
        match.current_position_y = 10
    else:
        kicking_team = match.team2
        direction = -1
        match.current_position_y = 110

    match.current_position_x = 35

    if match.current_seconds >= 2400 and match.current_half == 1:
        return {"event": "half_time"}
    elif match.current_seconds >= 4800:
        return {"event": "full_time"}
    
    match.current_tackle_count = 1
    kicker = max(kicking_team.players, key=lambda p: p.long_kicking)
    
    # Base distance that a perfect kick would travel
    base_distance = 50
    
    # Adjust base distance by a random factor influenced by the kicker's skill
    random_factor = random.uniform(-20, 20)  # Introduce variability from -20 to +20 metres
    skill_adjustment = kicker.long_kicking / 100  # Skill adjustment based on kicker's ability, normalised between 0 and 1
    
    # Calculate kick distance considering skill adjustment
    kick_distance = base_distance + random_factor * (1 - skill_adjustment)
    
    # Ensure kick distance is within 10 to 70 metres
    kick_distance = min(max(kick_distance, 10), 70)
    
    match.current_position_y += ( direction * kick_distance )
    log_event(match, f"{kicker.name} kicks off from behind the posts.", 30)
    match.current_position_x = random.uniform(1, 69)
    return {"event": "catch_kick", "kicker": kicker, "kick_type": "drop out", "kick_distance": kick_distance, "kick_height": 0}
