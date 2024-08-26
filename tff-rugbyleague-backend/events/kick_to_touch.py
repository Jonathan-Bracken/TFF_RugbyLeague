# events/kick_to_touch.py

import random

def kick_to_touch(match):
    from events.log_event import log_event

    if match.current_team_possession == 1:
            attacking_team = match.team1
            distance_from_line = 110 - match.current_position_y
            direction = 1
    else:
            attacking_team = match.team2
            distance_from_line = match.current_position_y - 10
            direction = -1
    
    kicker = max(attacking_team.players, key=lambda p: p.long_kicking)

    if (distance_from_line < 20):
        log_event(match, f"{kicker.name} taps the ball.", 20, 3)
    else:        
        # Base distance is influenced by kicker's long kicking ability and the position on the pitch
        base_kick_distance = 50 * (kicker.long_kicking / 100) * (1 - ((abs(match.current_position_x - 35) + 30)/100))
        
        # Calculate the actual kick distance with some randomness
        random_factor = random.uniform(0.5, 1.5)
        kick_distance = base_kick_distance * random_factor
        kick_distance = min(max(kick_distance, 0), distance_from_line - 10)  # Ensure distance is within valid range
        
        # Update the current position tentatively
        new_position_y = match.current_position_y + ( direction * kick_distance )

        previous_position_x = match.current_position_x
        match.current_position_x = 0 if match.current_position_x < 35 else 70
        match.current_position_y = new_position_y
        log_event(match, f"{kicker.name} kicks to touch. Ball travels {kick_distance:.0f} metres.", 20, 3)
    
        # Update the current position
        match.current_position_x = previous_position_x
        log_event(match, f"{kicker.name} taps the ball.", 0, 3)
    
    # Go to dummy half play
    return {"event": "dummy_half", "ball_player": kicker}