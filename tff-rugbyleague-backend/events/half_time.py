# events/half_time.py

def half_time(match):
    from events.log_event import log_event
    
    log_event(match, f"The referee blows the whistle for half time.", 0, 5)
    match.current_team_possession = 2
    match.current_seconds = 2400
    match.current_half = 2