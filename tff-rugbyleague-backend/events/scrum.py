# events/scrum.py

import random
def scrum(match):
    from events.log_event import log_event

    if match.current_seconds >= 2400 and match.current_half == 1:
        return {"event": "half_time"}
    elif match.current_seconds >= 4800:
        return {"event": "full_time"}

    match.current_tackle_count = 1
    match.current_position_x = 35
    match.current_position_y = min(max(match.current_position_y, 20), 100)

    if match.current_team_possession == 1:
        attacking_team = match.team1
        defending_team = match.team2
    else:
        attacking_team = match.team2
        defending_team = match.team1

    halfback = [p for p in attacking_team.players if p.position == "Half Back" and not p.interchange][0]
    if halfback == None:
        halfback = [p for p in attacking_team.players if p.position == "Stand Off" and not p.interchange][0]
    if halfback == None:
        halfback = [p for p in attacking_team.players if p.position == "Full Back" and not p.interchange][0]

    if random.random() < 0.98:  # 98% chance of successful scrum
        log_event(match, f"{halfback.name} feeds the scrum for {attacking_team.name}.", 5, 5)
        next_player = random.choice(
            [
                p
                for p in attacking_team.players
                if p.position not in ["Prop", "Right Second Row", "Left Second Row", "Loose Forward", "Hooker", "Left Wing", "Right Wing"]
                and p is not halfback
                and not p.interchange
            ]
        )
        return {"event": "pass_ball", "passer": halfback, "target": next_player, "next_play": "attacking move"}
    else:
        log_event(match, f"The scrum collapses. Penalty to {defending_team.name}.", 10, 5)
        return {"event": "penalty"}