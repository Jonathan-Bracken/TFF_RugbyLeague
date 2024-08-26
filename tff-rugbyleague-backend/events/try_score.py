# events/try_score.py

def try_score(match):
    from events.log_event import log_event
    
    if match.current_team_possession == 1:
        scoring_team = match.team1
    else:
        scoring_team = match.team2

    scoring_team.score += 4
    log_event(match, f"Score update: {match.team1.name} {match.team1.score}-{match.team2.name} {match.team2.score}", 30, 3)
    return {"event": "conversion_kick"}