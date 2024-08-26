# events/short_kick.py

import random

def short_kick(match, kicker, ball_player):
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

    if (random.random()) < 0.5:
        full_back = next(
            (player for player in defending_team.players if player.position == "Full Back"),
            None,
        )
    else:
        full_back = random.choice([p for p in defending_team.players if not p.interchange])
    if full_back == None:
        full_back = random.choice([p for p in defending_team.players if not p.interchange])

    chaser = random.choice([p for p in attacking_team.players if not p.interchange and p is not ball_player])

    kick_distance = distance_from_line + (10 - ( kicker.short_kicking / 10 )) + random.uniform(0, 10)
    chance_of_miskick = 0.5 * (1 - (kicker.short_kicking / 100))

    if chance_of_miskick > random.random():
        match.current_position_x = min(max(match.current_position_x + random.uniform(-2, 2), 1), 69)
        match.current_team_possession = 1 if match.current_team_possession == 2 else 2
        match.current_tackle_count = 1
        kicker.rating = min(max(kicker.rating - 2, 0), 100)
        log_event(match, f"{kicker.name} tries to kick but loses the ball. {full_back.name} collects it.", 1, 3)
        return { "event": "tackled", "ball_carrier": full_back, "tackler": chaser }
    else:
        match.current_position_x = min(max(match.current_position_x + random.uniform(-5, 5), 1), 69)
        match.current_position_y += (direction * kick_distance)
        log_event(match, f"{kicker.name} grubber kicks the ball into the in-goal area.", 1, 3)
        if kick_distance >= distance_from_line + 10:
            match.current_position_x = 35
            match.current_position_y = 30 if match.current_team_possession == 2 else 90
            match.current_team_possession = 1 if match.current_team_possession == 2 else 2
            match.current_tackle_count = 1
            log_event(match, f"The kick from {kicker.name} goes dead in goal. {defending_team.name} have the 20 metre restart.", 1, 3)
            return { "event": "dummy_half", "ball_player": full_back }
        elif random.random() < kicker.short_kicking / 150 and random.random() < chaser.instinct / 150:
            if random.random() < full_back.instinct / 50:
                kicker.rating = min(max(kicker.rating + 2, 0), 100)
                chaser.rating = min(max(chaser.rating + 2, 0), 100)
                full_back.rating = min(max(full_back.rating + 2, 0), 100)
                match.current_team_possession = 1 if match.current_team_possession == 2 else 2
                log_event(match, f"{full_back.name} reaches the ball first and concedes a drop out.", 1, 3)
                return {"event": "drop_out"}
            else:
                kicker.rating = min(max(kicker.rating + 4, 0), 100)
                chaser.rating = min(max(chaser.rating + 4, 0), 100)
                full_back.rating = min(max(full_back.rating - 4, 0), 100)
                log_event(match, f"{chaser.name} reaches the ball first and scores the try!", 1, 3)
                return {"event": "try_scored"}
        else:
            if random.random() < full_back.instinct / 150:
                match.current_team_possession = 1 if match.current_team_possession == 2 else 2
                match.current_tackle_count = 1
                kicker.rating = min(max(kicker.rating - 2, 0), 100)
                chaser.rating = min(max(chaser.rating - 2, 0), 100)
                full_back.rating = min(max(full_back.rating + 2, 0), 100)
                log_event(match, f"{full_back.name} collects the kick easily.", 1, 3)
                return { "event": "tackled", "ball_carrier": full_back, "tackler": chaser }
            else:
                match.current_team_possession = 1 if match.current_team_possession == 2 else 2
                kicker.rating = min(max(kicker.rating - 2, 0), 100)
                chaser.rating = min(max(chaser.rating - 2, 0), 100)
                full_back.rating = min(max(full_back.rating - 2, 0), 100)
                log_event(match, f"{chaser.name} collects the kick but knocks on!", 1)
                return { "event": "knock_on" }