# events/pass_ball.py

import random

def pass_ball(match, passer, target, next_play):
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

    # Calculate the possibility of the catcher immediately knocking on
    knock_on_possibility = 0.2 * (1 - (target.catching / 100)) * (1 - (passer.passing / 100))

    if random.random() < knock_on_possibility:
        passer.rating = min(max(passer.rating - 2, 0), 100)
        target.rating = min(max(target.rating - 2, 0), 100)
        log_event(
            match,
            f"{target.name} drops the pass. It's a scrum for {defending_team.name}.",
            25,
            5
        )
        match.current_team_possession = 1 if match.current_team_possession == 2 else 2
        return {"event": "knock_on"}

    if next_play == "long kick":
        return {"event": "long_kick", "kicker": target}

    if next_play == "short kick":
        return {"event": "short_kick", "kicker": target, "ball_player": None}

    if next_play == "bomb kick":
        return {"event": "bomb_kick", "kicker": target}

    if next_play == "hit up":
        # Attempt to move back towards the centre of the pitch if catching the ball out wide
        if match.current_position_x < 20:
            match.current_position_x = match.current_position_x + random.uniform(0,20)
            tackler = random.choice(
                [
                    p
                    for p in defending_team.players
                    if ((p.position in ["Left Second Row", "Left Centre"] and match.current_team_possession == 2)
                    or (p.position in ["Right Second Row", "Right Centre"] and match.current_team_possession == 1))
                    and not p.interchange
                ]
            )
        elif match.current_position_x > 50:
            match.current_position_x = match.current_position_x - random.uniform(0,20)
            tackler = random.choice(
                [
                    p
                    for p in defending_team.players
                    if ((p.position in ["Left Second Row", "Left Centre"] and match.current_team_possession == 1)
                    or (p.position in ["Right Second Row", "Right Centre"] and match.current_team_possession == 2))
                    and not p.interchange
                ]
            )
        else:
            match.current_position_x = match.current_position_x - random.uniform(-20,20)
            tackler = random.choice(
                [
                    p
                    for p in defending_team.players
                    if p.position in ["Prop", "Hooker", "Loose Forward", "Stand Off", "Half Back"]
                    and not p.interchange
                ]
            )
        return {"event": "tackled", "ball_carrier": target, "tackler": tackler}

    if next_play == "attacking move":
        tackler = random.choice(
            [
                p
                for p in defending_team.players
                if ((p.position in ["Left Centre", "Left Wing", "Full Back"] and match.current_team_possession == 1)
                or (p.position in ["Right Centre", "Right Wing", "Full Back"] and match.current_team_possession == 2))
                and not p.interchange
            ]
        ) if match.current_position_x < 10 else random.choice(
            [
                p
                for p in defending_team.players
                if (p.position in ["Right Centre", "Right Wing", "Full Back"] and match.current_team_possession == 1)
                or (p.position in ["Left Centre", "Left Wing", "Full Back"] and match.current_team_possession == 2)
                and not p.interchange
            ]
        ) if match.current_position_x > 60 else random.choice(
            [
                p
                for p in defending_team.players
                if (p.position in ["Left Centre", "Left Second Row"] and match.current_team_possession == 1)
                or (p.position in ["Right Centre", "Right Second Row"] and match.current_team_possession == 2)
                and not p.interchange
            ]
        ) if match.current_position_x < 20 else random.choice(
            [
                p
                for p in defending_team.players
                if (p.position in ["Right Centre", "Right Second Row"] and match.current_team_possession == 1)
                or (p.position in ["Left Centre", "Left Second Row"] and match.current_team_possession == 2)
                and not p.interchange
            ]
        ) if match.current_position_x > 50 else random.choice(
            [
                p
                for p in defending_team.players
                if p.position not in ["Right Centre", "Right Wing", "Left Centre", "Left Wing"]
                and not p.interchange
            ]
        )
        
        # If the ball goes out wide
        if match.current_position_x < 8 or match.current_position_x > 62:
            if distance_from_line <= 10:
                log_event(match, f"{target.name} goes for the corner!", 2, 2)
                finishing_ability = (
                    target.pace + target.side_stepping + target.instinct + target.strength
                ) / 400
                passing_ability = passer.passing / 100
                defending_ability = (tackler.pace + tackler.tackling) / 200
                if random.random() < finishing_ability and random.random() < passing_ability:
                    if random.random() > defending_ability:
                        tackler.rating = min(max(tackler.rating - 2, 0), 100)
                        passer.rating = min(max(passer.rating + 2, 0), 100)
                        target.rating = min(max(target.rating + 2, 0), 100)
                        match.current_position_y += (direction * 10)
                        return { "event": "line_break", "ball_carrier": target }
                    else:
                        tackler.rating = min(max(tackler.rating + 2, 0), 100)
                        match.current_position_y += (direction * 5)
                        log_event(match, f"{tackler.name} makes a desperate tackle!", 2, 2)
                        return {"event": "tackled", "ball_carrier": target, "tackler": tackler}
                elif random.random() < defending_ability:
                    tackler.rating = min(max(tackler.rating + 3, 0), 100)
                    passer.rating = min(max(passer.rating - 1, 0), 100)
                    target.rating = min(max(passer.rating - 1, 0), 100)
                    match.current_position_y += (direction * (distance_from_line + 5))
                    log_event(
                        match,
                        f"{tackler.name} makes a huge tackle and forces {target.name} out of play!",
                        0,
                        5
                    )
                    match.current_team_possession = 1 if match.current_team_possession == 2 else 2
                    return { "event": "knock_on" }
                else:
                    tackler.rating = min(max(tackler.rating + 1, 0), 100)
                    passer.rating = min(max(passer.rating - 1, 0), 100)
                    target.rating = min(max(passer.rating - 1, 0), 100)
                    log_event(match, f"{tackler.name} makes a desperate tackle!", 2, 5)
                    return {"event": "tackled", "ball_carrier": target, "tackler": tackler}
            else:
                # Otherwise, cut back inside
                match.current_position_x = match.current_position_x + random.uniform(0, 20) if match.current_position_x < 10 else match.current_position_x - random.uniform(0, 20)
                log_event(match, f"{target.name} cuts back inside.", 2, 2)
                return {"event": "tackled", "ball_carrier": target, "tackler": tackler}
        elif match.current_position_x < 15 or match.current_position_x > 55:
            # If the ball is within 20 metres of the touchline, decide whether or not to pass the ball further wide
            if random.random() > (distance_from_line / 100) + (passer.passing / 100):
                match.current_position_x = match.current_position_x + 10 if match.current_position_x > 50 else match.current_position_x - 10
                new_target = random.choice(
                    [
                        p
                        for p in attacking_team.players
                        if ((p.position in ["Left Centre", "Left Wing"] and match.current_team_possession == 1)
                        or (p.position in ["Right Centre", "Right Wing"] and match.current_team_possession == 2))
                        and p is not target
                        and not p.interchange
                    ]
                ) if match.current_position_x < 20 else random.choice(
                    [
                        p
                        for p in attacking_team.players
                        if ((p.position in ["Right Centre", "Right Wing"] and match.current_team_possession == 1)
                        or (p.position in ["Left Centre", "Left Wing"] and match.current_team_possession == 2))
                        and p is not target
                        and not p.interchange
                    ]
                )
                log_event(match, f"{target.name} throws the ball wide to {new_target.name}!", 2, 2)
                return {"event": "pass_ball", "passer": target, "target": new_target, "next_play": "attacking move"}
            elif distance_from_line <= 10:
                match.current_position_x += random.uniform(-10, 10)
                log_event(match, f"{target.name} goes for the line!", 2, 2)
                return {"event": "tackled", "ball_carrier": target, "tackler": tackler}
            else:
                match.current_position_x = match.current_position_x + random.uniform(0, 10) if match.current_position_x < 35 else match.current_position_x - random.uniform(0,10)
                match.current_position_y += (direction * random.uniform(0, 5))
                log_event(match, f"{target.name} carries the ball forward.", 2, 2)
                return {"event": "tackled", "ball_carrier": target, "tackler": tackler}
        elif random.random() < ( target.short_kicking / 200 ) and match.current_tackle_count == 5 and distance_from_line < 20:
            match.current_position_x = match.current_position_x + random.uniform(-10, 10)
            return {"event": "short_kick", "kicker": target, "ball_player": None}
        elif random.random() < ( target.short_kicking / 1000 ) and match.current_tackle_count in [3, 4] and distance_from_line < 20:
            match.current_position_x = match.current_position_x + random.uniform(-10, 10)
            log_event(match, f"{target.name} opts for an early kick!", 0, 0)
            return {"event": "short_kick", "kicker": target, "ball_player": None}
        elif random.random() < ( target.long_kicking / 100 ) and match.current_tackle_count == 5 and distance_from_line > 40:
            match.current_position_x = match.current_position_x + random.uniform(-10, 10)
            return {"event": "long_kick", "kicker": target, "ball_player": None}
        elif random.random() < ( target.long_kicking / 500 ) and match.current_tackle_count in [3, 4] and distance_from_line > 40:
            match.current_position_x = match.current_position_x + random.uniform(-10, 10)
            log_event(match, f"{target.name} opts for an early kick!", 0, 0)
            return {"event": "long_kick", "kicker": target, "ball_player": None}
        elif random.random() < ( target.passing / 100 ):
            match.current_position_x = match.current_position_x + (random.uniform(10, 20) * random.choice([1, -1]))
            match.current_position_y += (direction * random.uniform(-5, 0))
            new_target = random.choice(
                [
                    p
                    for p in attacking_team.players
                    if ((p.position in ["Left Centre", "Left Wing"] and match.current_team_possession == 1)
                    or (p.position in ["Right Centre", "Right Wing"] and match.current_team_possession == 2))
                    and p is not target and p is not passer
                    and not p.interchange
                ]
            ) if match.current_position_x < 10 else random.choice(
                [
                    p
                    for p in attacking_team.players
                    if ((p.position in ["Right Centre", "Right Wing"] and match.current_team_possession == 1)
                    or (p.position in ["Left Centre", "Left Wing"] and match.current_team_possession == 2))
                    and p is not target and p is not passer
                    and not p.interchange
                ]
            ) if match.current_position_x > 60 else random.choice(
                [
                    p
                    for p in attacking_team.players
                    if ((p.position in ["Right Centre", "Right Second Row", "Stand Off", "Full Back"] and match.current_team_possession == 1)
                    or (p.position in ["Left Centre", "Left Second Row", "Half Back", "Full Back"] and match.current_team_possession == 2))
                    and p is not target and p is not passer
                    and not p.interchange
                ]
            ) if match.current_position_x < 20 else random.choice(
                [
                    p
                    for p in attacking_team.players
                    if ((p.position in ["Left Centre", "Left Second Row", "Half Back", "Full Back"] and match.current_team_possession == 1)
                    or (p.position in ["Right Centre", "Right Second Row", "Stand Off", "Full Back"] and match.current_team_possession == 2))
                    and p is not target and p is not passer
                    and not p.interchange
                ]
            ) if match.current_position_x > 50 else random.choice(
                [
                    p
                    for p in attacking_team.players
                    if p.position not in ["Right Wing", "Left Wing", "Right Centre", "Left Centre"]
                    and p is not target and p is not passer
                    and not p.interchange
                ]
            )
            log_event(match, f"{target.name} passes the ball on to {new_target.name}.", 2, 2)
            return {"event": "pass_ball", "passer": target, "target": new_target, "next_play": "attacking move"}
        else:
            match.current_position_x = match.current_position_x + random.uniform(-10, 10)
            log_event(match, f"{target.name} carries the ball forward.", 2, 2)
            return {"event": "tackled", "ball_carrier": target, "tackler": tackler}