# events/meet_defence.py

import math
import random

def meet_defence(match, ball_carrier, tackler, defence_distance = 10):
    from events.log_event import log_event

    direction = 1 if match.current_team_possession == 1 else 2

    if (defence_distance == 0):
        # If the defence are immediately around the catcher, move straight to attempted tackle
        log_event(match, f"{ball_carrier.name} is immediately surrounded by defenders.", 0, 3)
        return {"event": "tackled", "ball_carrier": ball_carrier, "tackler": tackler}
    else:   
        log_event(match, f"{ball_carrier.name} carries the ball forward.", math.floor(defence_distance / 10), 0)
        
        # Attempt to move back towards the centre of the pitch if catching the ball out wide
        if (match.current_position_x < 20):
            match.current_position_x = match.current_position_x + random.uniform(0, 20)
        if (match.current_position_x > 70):
            match.current_position_x = match.current_position_x + random.uniform(0, 20)
        else:
            match.current_position_x = match.current_position_x + random.uniform(-10, 10)

    if (defence_distance > 10):
        # Adjust base distance by ball_carrier's speed, introduce variability
        speed_factor = ball_carrier.pace / 200
        random_factor = random.uniform(0.5, 1.5)
        
        metres_made = defence_distance * ( speed_factor * random_factor )
        
        # Update the position based on the direction and metres made
        match.current_position_y += ( direction * metres_made )
        
        # Ensure position is within field limits (0 to 100 metres)
        match.current_position_y = min(max(match.current_position_y, 0), 100)

    # Calculate the ball carrier's and tackler's effectiveness
    ball_carrier_effectiveness = (ball_carrier.strength + ball_carrier.side_stepping + ball_carrier.instinct) / 3000
    tackler_effectiveness = (tackler.tackling + tackler.strength) / 2000
    
    # Calculate the probability of a line break based on the effectiveness of both players    
    if random.random() > tackler_effectiveness and random.random() < ball_carrier_effectiveness:
        ball_carrier.rating = min(max(ball_carrier.rating + 2, 0), 100)
        tackler.rating = min(max(tackler.rating - 2, 0), 100)
        log_event(match, f"{ball_carrier.name} avoids the tackle from {tackler.name}!", 0, 2)
        return {"event": "line_break", "ball_carrier": ball_carrier}
    else:
        return {"event": "tackled", "ball_carrier": ball_carrier, "tackler": tackler}
        