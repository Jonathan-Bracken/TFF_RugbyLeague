# events/line_break.py

import random

def line_break(match, ball_carrier):
    from events.log_event import log_event

    if match.current_team_possession == 1:
        defending_team = match.team2
        direction = 1
        distance_from_line = 110 - match.current_position_y
    else:
        defending_team = match.team1
        direction = -1
        distance_from_line = match.current_position_y - 10

    # Opposition fullback
    fullback = next((player for player in defending_team.players if player.position == "Full Back"), None)

    base_distance = 20
    
    # Determine if the player is close to scoring a try
    if distance_from_line <= 10:
        from lists import line_break_near_line
        line_break_description = random.choice(line_break_near_line)
        match.current_position_y = min(max(match.current_position_y + (base_distance * direction), 115), 5)
        log_event(match, f"{ball_carrier.name} {line_break_description} and scores the try!", 5, 5)
        return {"event": "try_scored"}
    elif distance_from_line <= 20:
        from lists import line_break_near_line
        line_break_description = random.choice(line_break_near_line)
        log_event(match, f"{ball_carrier.name} {line_break_description} and goes for the try line!", 5, 3)
        match.current_position_y = min(max(match.current_position_y + (base_distance * direction), 115), 5)

        # Determine, based on variability and the skill of both players, whether the player scores a try or is stopped
        if random.random() < fullback.tackling / 200:
            fullback.rating = min(max(fullback.rating + 2, 0), 100)
            log_event(match, f"{fullback.name} stops {ball_carrier.name} just short of the line!", 1, 5)
            return {"event": "tackled", "ball_carrier": ball_carrier, "tackler": fullback}
        elif random.random() < ( ball_carrier.pace + ball_carrier.side_stepping + ball_carrier.instinct ) / 300:
            ball_carrier.rating = min(max(ball_carrier.rating + 5, 0), 100)
            fullback.rating = min(max(fullback.rating - 2, 0), 100)
            from lists import try_put_down
            try_score_description = random.choice(try_put_down)
            log_event(match, f"{ball_carrier.name} {try_score_description} and scores the try!", 1, 5)
            return {"event": "try_scored"}
        elif random.random() < ball_carrier.instinct / 100:
            fullback.rating = min(max(fullback.rating + 2, 0), 100)
            log_event(match, f"{fullback.name} stops {ball_carrier.name} just short of the line!", 1, 5)
            return {"event": "tackled", "ball_carrier": ball_carrier, "tackler": fullback}
        else:
            log_event(match, f"{ball_carrier.name} loses the ball close to the line!", 1, 5)
            ball_carrier.rating = min(max(ball_carrier.rating - 2, 0), 100)
            match.current_position_y = 30 if match.current_team_possession == 2 else 90
            match.current_team_possession = 1 if match.current_team_possession == 2 else 2
            return {"event": "knock_on_over_line"}
    else:
        # If the ball carrier can beat the fullback with a sidestep
        if (1 - ((ball_carrier.pace + ball_carrier.side_stepping) * 800) < random.random()) and (fullback.tackling / 100 < random.random()):
            fullback.rating = min(max(fullback.rating - 4, 0), 100)
            from lists import line_break_beat_fullback
            line_break_description = random.choice(line_break_beat_fullback)
            match.current_position_y = match.current_position_y + (base_distance * direction)
            log_event(match, f"{ball_carrier.name} {line_break_description} {fullback.name} and runs clear!", 5, 5)

            # Calculate whether the ball carrier can outrun the fastest defender based on speed and distance to tryline
            fastest_defender = max([p for p in defending_team.players if p is not fullback and not p.interchange], key=lambda p: p.pace)
            
            if ball_carrier.pace + ((100 - distance_from_line)/10) > fastest_defender.pace and fastest_defender.tackling / 100 * random.uniform(1, 1.5) > random.random():
                ball_carrier.rating = min(max(ball_carrier.rating + 10, 0), 100)
                match.current_position_y = 5 if defending_team == 1 else 115
                from lists import breakaway_try_superlatives
                try_score_description = random.choice(breakaway_try_superlatives)
                log_event(match, f"{ball_carrier.name} scores a {try_score_description} solo try!", distance_from_line / 10, 5)
                return {"event": "try_scored"}
            else:
                ball_carrier.rating = min(max(ball_carrier.rating + 5, 0), 100)
                fastest_defender.rating = min(max(fastest_defender.rating + 5, 0), 100)
                match.current_position_y += direction * (random.uniform(5, distance_from_line))
                log_event(match, f"{ball_carrier.name} is finally tackled by {fastest_defender.name}!", distance_from_line / 10, 5)
                return {"event": "tackled", "ball_carrier": ball_carrier, "tackler": fastest_defender}
        else:
            match.current_position_y = match.current_position_y + (base_distance * direction)
            log_event(match, f"{fullback.name} tackles {ball_carrier.name}!", 5, 5)
            return {"event": "tackled", "ball_carrier": ball_carrier, "tackler": fullback}