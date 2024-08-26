# events/dummy_half.py

import random

def dummy_half(match, ball_player):
    from events.log_event import log_event

    if match.current_team_possession == 1:
        attacking_team = match.team1
        defending_team = match.team2
        distance_from_line = 110 - match.current_position_y
    else:
        attacking_team = match.team2
        defending_team = match.team1
        distance_from_line = match.current_position_y - 10
    
    # The hooker should be the designated hooker or a random replacement if the hooker is playing the ball
    hooker = next((p for p in attacking_team.players if p.position == "Hooker" and not p.interchange and p is not ball_player), None)
    if hooker is None:
        hooker = random.choice(
            [
                p for p in attacking_team.players
                if not p.interchange
                and p is not ball_player
            ]
        )

    # Calculate the probability of the hooker knocking on
    knock_on_prob = max(((200 - hooker.passing - hooker.catching) / 10000), 0.005)  # Minimum 0.5% chance

    if random.random() < knock_on_prob:
        hooker.rating = min(max(hooker.rating - 4, 0), 100)
        match.current_tackle_count = 1
        match.current_team_possession = 1 if match.current_team_possession == 2 else 2
        log_event(match, f"{hooker.name} knocks on at the play the ball. Scrum to {defending_team.name}.", 15, 5)
        return {"event": "knock_on"}

    available_players = [p for p in attacking_team.players if p is not hooker and not p.interchange and p is not ball_player]
    forwards = [p for p in available_players if p is not hooker and p.position in ["Prop", "Loose Forward", "Right Second Row", "Left Second Row"]]
    long_kicker = max(available_players, key=lambda p: p.long_kicking)
    short_kicker = max(available_players, key=lambda p: p.short_kicking)
    playmaker = random.choice(
        [
            p
            for p in available_players
            if p.position in ["Hooker", "Half Back", "Stand Off", "Full Back"]
        ]
    )    
    defender = random.choice(
        [
            p
            for p in defending_team.players
            if ((p.position in ["Hooker", "Half Back", "Stand Off", "Full Back", "Prop", "Loose Forward"]
            and match.current_position_x > 20 and match.current_position_x < 50)
            or (p.position in ["Right Centre", "Right Second Row", "Right Wing"]
            and match.current_position_x <= 20 and match.current_team_possession == 1)
            or (p.position in ["Left Centre", "Left Second Row", "Left Wing"]
            and match.current_position_x <= 20 and match.current_team_possession == 2)
            or (p.position in ["Left Centre", "Left Second Row", "Left Wing"]
            and match.current_position_x >= 50 and match.current_team_possession == 1)
            or (p.position in ["Right Centre", "Right Second Row", "Right Wing"]
            and match.current_position_x >= 50 and match.current_team_possession == 2))
            and not p.interchange
        ]
    )
    
    if match.current_tackle_count == 5:
        if random.random() < 0.05 + hooker.long_kicking / 1000 and distance_from_line > 40:
            return { "event": "long_kick", "kicker": hooker }
        elif random.random() < 0.1 + hooker.short_kicking / 1000 and distance_from_line <= 20:
            return { "event": "short_kick", "kicker": hooker, "ball_player": ball_player }
        elif distance_from_line > 50:
            if random.random() < 0.9:
                return { "event": "pass_ball", "passer": hooker, "target": long_kicker, "next_play": "long kick" }
            else:
                return { "event": "pass_ball", "passer": hooker, "target": playmaker, "next_play": "attacking move" }
        elif distance_from_line > 20:
            if random.random() < 0.8:
                return { "event": "pass_ball", "passer": hooker, "target": long_kicker, "next_play": "bomb kick" }
            else:
                return { "event": "pass_ball", "passer": hooker, "target": playmaker, "next_play": "attacking move" }
        else:
            if random.random() < 0.4:
                return { "event": "pass_ball", "passer": hooker, "target": playmaker, "next_play": "attacking move" }
            else:
                return { "event": "pass_ball", "passer": hooker, "target": short_kicker, "next_play": "short kick" }
    elif distance_from_line <= 10:
        if random.random() < 0.1:
            return { "event": "tackled", "ball_carrier": hooker, "tackler": defender }
        elif random.random() < 0.5:
            return { "event": "pass_ball", "passer": hooker, "target": playmaker, "next_play": "attacking move" }
        else:
            return { "event": "pass_ball", "passer": hooker, "target": random.choice(forwards), "next_play": "hit up" }
    elif distance_from_line <= 20:
        if random.random() < 0.4:
            return { "event": "pass_ball", "passer": hooker, "target": playmaker, "next_play": "attacking move" }
        else:
            return { "event": "pass_ball", "passer": hooker, "target": random.choice(forwards), "next_play": "hit up" }
    else:
        if random.random() < 0.1:
            return { "event": "pass_ball", "passer": hooker, "target": playmaker, "next_play": "attacking move" }
        else:
            return { "event": "pass_ball", "passer": hooker, "target": random.choice(forwards), "next_play": "hit up" }