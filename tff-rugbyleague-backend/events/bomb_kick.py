# events/long_kick.py

import math
import random

def bomb_kick(match, kicker):
    from events.log_event import log_event

    if match.current_team_possession == 1:
        distance_from_line = 110 - match.current_position_y
        direction = 1
    else:
        distance_from_line = match.current_position_y - 10
        direction = -1
    
    skill_adjustment = kicker.long_kicking / 100

    # Base distance is influenced by kicker's long kicking ability and the position on the pitch
    base_kick_distance_y = min(distance_from_line, 30)
    base_kick_distance_x = match.current_position_x - 10 if match.current_position_x < 35 else 60 - match.current_position_x
    base_height = 10

    # Calculate the actual kick distance with some randomness
    random_factor_y = random.uniform(-20, 0)
    random_factor_x = random.uniform(-10, 10)
    random_factor_height = random.uniform(0, 10)
    
    kick_distance_y = base_kick_distance_y + ( random_factor_y * ( 1 - skill_adjustment ))
    kick_distance_x = base_kick_distance_x + ( random_factor_x * ( 1 - skill_adjustment ))
    kick_height = base_height - ( random_factor_height * ( 1 - skill_adjustment ))
    
    # Update the current position tentatively
    new_position_y = match.current_position_y + (direction * kick_distance_y)
    new_position_x = match.current_position_x - kick_distance_x if match.current_position_x < 35 else match.current_position_x + kick_distance_x

    if new_position_x < 0 or new_position_x > 70:
        log_event(match, f"{kicker.name} kicks the bomb out on the full. Scrum to {defending_team.name}.", math.floor(kick_distance_y / 20), 5)
    else:
        match.current_position_y = new_position_y
        match.current_position_x = new_position_x
        log_event(match, f"{kicker.name} kicks the ball high.", math.floor(kick_height), 3)
        return { "event": "catch_kick", "kicker": kicker, "kick_type": "bomb kick", "kick_distance": kick_distance_y, "kick_height": kick_height }
