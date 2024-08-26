# events/attempt_tackle.py

import random

def attempt_tackle(match, ball_carrier, tackler):
    from events.log_event import log_event

    if match.current_team_possession == 1:
        attacking_team = match.team1
        defending_team = match.team2
        direction = 1
        distance_from_line = 110 - match.current_position_y
    else:
        attacking_team = match.team2
        defending_team = match.team1
        direction = -1
        distance_from_line = match.current_position_y - 10

    # Calculate fatigue increase based on fitness and random factor
    ball_carrier_fatigue_increase = round(random.uniform(0.5, 1) * (1 - ball_carrier.fitness / 100), 1)
    tackler_fatigue_increase = round(random.uniform(1, 2) * (1 - tackler.fitness / 100), 1)
    
    ball_carrier.fatigue += ball_carrier_fatigue_increase
    tackler.fatigue += tackler_fatigue_increase

    # Calculate the probability of a dangerous tackle
    dangerous_tackle_prob = max((1 - (tackler.discipline / 100)) * 0.1, 0.01)  # Minimum 1% chance
    
    if random.random() < dangerous_tackle_prob:
        tackler.rating = min(max(tackler.rating - 5, 0), 100)
        match.current_tackle_count = 1
        match.current_position_y = min(max(match.current_position_y, 20), 100)
        log_event(match, f"{tackler.name} makes a dangerous tackle on {ball_carrier.name}. Penalty to {attacking_team.name}.", 5)
        return {"event": "penalty"}
    
    # Calculate the probability of the player knocking on
    knock_on_prob = max(tackler.tackling / 1000 + ((1-ball_carrier.strength) / 1000), 0.01)  # Minimum 1% chance

    if random.random() < knock_on_prob:
        ball_carrier.rating = min(max(ball_carrier.rating - 4, 0), 100)
        tackler.rating = min(max(tackler.rating + 2, 0), 100)
        match.current_tackle_count = 1
        match.current_team_possession = 1 if match.current_team_possession == 2 else 2
        log_event(match, f"The tackle from {tackler.name} causes {ball_carrier.name} to lose the ball. Scrum to {defending_team.name}.", 15, 5)
        return {"event": "knock_on"}
    
    # Random factor to introduce variability in metres gained
    random_factor = random.uniform(-5, 5)
    
    # Calculate metres gained based on strength and random factor
    metres_gained = (ball_carrier.strength / 5) - (tackler.tackling / 40 + tackler.strength / 40) + random_factor
    # If close to the line, defence will be intensified
    if distance_from_line <= 10:
        metres_gained = metres_gained / 2

    match.current_position_y += ( direction * metres_gained )
    
    ball_carrier.rating = min(max(ball_carrier.rating + (metres_gained/10), 0), 100)
    tackler.rating = min(max(tackler.rating + 1-(metres_gained/10), 0), 100)

    distance_from_line = 110 - match.current_position_y if match.current_team_possession == 1 else match.current_position_y - 10

    if distance_from_line <= 0:
        log_event(match, f"{ball_carrier.name} is going for the line!", 1, 2)
        if random.random() < ball_carrier.strength / 100 and random.random() > tackler.strength / 100:
            ball_carrier.rating = min(max(ball_carrier.rating + 5, 0), 100)
            tackler.rating = min(max(tackler.rating - 5, 0), 100)
            from lists import power_play_try
            description = random.choice(power_play_try)
            log_event(match, f"{ball_carrier.name} {description} and scores the try!", 5, 5)
            return {"event": "try_scored"}
        else:
            tackler.rating = min(max(tackler.rating + 2, 0), 100)
            match.current_position_y = 100 if match.current_team_possession == 1 else 20
            log_event(match, f"{ball_carrier.name} is held up over the line by {tackler.name}!", 5, 5)
            
            if match.current_seconds >= 2400 and match.current_half == 1:
                return {"event": "half_time"}
            elif match.current_seconds >= 4800:
                return {"event": "full_time"}
            
            match.current_tackle_count += 1
            if match.current_tackle_count >= 6:
                return {"event": "turnover"}
            else:
                return {"event": "dummy_half", "ball_player": ball_carrier}
    
    if metres_gained >= 5:
        log_event(match, f"{ball_carrier.name} makes a strong carry, tackled by {tackler.name}.", 5, 3)
    elif metres_gained >= 0:
        log_event(match, f"{ball_carrier.name} is tackled by {tackler.name}.", 5, 3)
    else:
        log_event(match, f"{ball_carrier.name} loses ground, tackled by {tackler.name}.", 5, 3)
    
    if match.current_seconds >= 2400 and match.current_half == 1:
        return {"event": "half_time"}
    elif match.current_seconds >= 4800:
        return {"event": "full_time"}

    match.current_tackle_count += 1
    if match.current_tackle_count >= 6:
        return {"event": "turnover"}
    else:
        return {"event": "dummy_half", "ball_player": ball_carrier}