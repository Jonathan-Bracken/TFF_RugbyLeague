# events/catch_kick.py

import random

def catch_kick(match, kicker, kick_type, kick_distance, kick_height):
    from events.log_event import log_event

    if kick_height is None:
        kick_height = 0

    if match.current_team_possession == 1:
        attacking_team = match.team1
        defending_team = match.team2
        current_position_x = 75 - match.current_position_x
    else:
        attacking_team = match.team2
        defending_team = match.team1
        current_position_x = match.current_position_x

    # If it is a kick to the corner, the wingers will cover it - unless it is an early kick, in which case they will not have dropped back.
    if (current_position_x < 20 and match.current_tackle_count in [1, 5]):
        catcher = next((player for player in defending_team.players if not player.interchange and player.position == "Left Wing"), None)
    elif (current_position_x > 70):
        catcher = next((player for player in defending_team.players if not player.interchange and player.position == "Right Wing"), None)
    # Otherwise, the full back will attempt the catch.
    else:
        catcher = next((player for player in defending_team.players if not player.interchange and player.position == "Full Back"), None)
    
    # If the winger or full back could not be found, replace with any other player in the team.
    if catcher == None:
        catcher = random.choice(
            [
                p
                for p in defending_team.players
                if not p.interchange
            ]
        )

    # Base probability of catching the ball depending on the type of kick
    base_catch_prob = 0.95 if kick_type == "kick off" or kick_type == "drop out" else 0.92 if kick_type == "long kick" else 0.8 if kick_type == "bomb" else 0.9

    # Adjust base probability by a random factor influenced by the skill of the kicker and catcher
    random_factor = random.uniform(0, (1-base_catch_prob)) 
    skill_adjustment = catcher.catching + ( 100 - kicker.long_kicking ) / 200 
    catch_prob = base_catch_prob + ( random_factor * skill_adjustment ) - (kick_height / 100)
    # Ensure catch probability is a minimum of 10%
    catch_prob = min(max(catch_prob, 0.1), 1)
    
    if random.random() < catch_prob:
        defence_distance = 0
                
        match.current_tackle_count = 1
        match.current_team_possession = 1 if match.current_team_possession == 2 else 2
        log_event(match, f"{catcher.name} catches the {kick_type}.", 0, 0)

        if kick_type == "kick off" or kick_type == "drop out" or kick_type == "long kick":
            defence_distance = kick_distance - (( kicker.long_kicking / 2 ) * random.uniform(0.5, 1))
            defence_distance = min(max(defence_distance, 0), 50)
            # Determine the likelihood of the player passing the ball on, or returning it themselves.
            if (random.random() < (catcher.strength / 100) and defence_distance > 0 and (kick_type == "kick off" or kick_type == "drop out")):
                new_player = random.choice([p for p in defending_team.players if p is not catcher and not p.interchange and p.position in ["Prop", "Left Second Row", "Right Second Row", "Loose Forward"]])
                match.current_position_x = match.current_position_x + random.uniform(5, 10) if match.current_position_x < 35 else match.current_position_x - random.uniform(5, 10)
                log_event(match, f"{catcher.name} passes the ball on to {new_player.name}.", 2, 3)
                catcher = new_player
        if kick_type == "bomb kick":
            catcher.rating = min(max(catcher.rating + 2, 0), 100)

        # Select a defender based on the current position of the ball
        if (current_position_x < 20):
            defender = random.choice([p for p in attacking_team.players if not p.interchange and p.position in ["Left Winger", "Left Centre", "Left Second Row"]])
            defence_distance = max(defence_distance - 5, 0)
        if (current_position_x > 70):
            defender = random.choice([p for p in attacking_team.players if not p.interchange and p.position in ["Right Winger", "Right Centre", "Right Second Row"]])
            defence_distance = max(defence_distance - 5, 0)
        else:
            defender = random.choice([p for p in attacking_team.players if not p.interchange and p.position in ["Prop", "Hooker", "Left Second Row", "Right Second Row", "Loose Forward", "Stand Off", "Half Back"]])        
        
        return {"event": "caught_kick", "ball_carrier": catcher, "tackler": defender, "defence_distance": defence_distance}
    else:
        if kick_type == "bomb kick":
            catcher.rating = min(max(catcher.rating - 2, 0), 100)
        else:
            catcher.rating = min(max(catcher.rating - 5, 0), 100)
            
        log_event(match, f"{catcher.name} drops the kick. Scrum to {defending_team.name}.", 15, 3)
        return {"event": "dropped_kick"}