# events/full_time.py

def full_time(match):
    from events.log_event import log_event
    
    log_event(match, f"The referee blows the whistle for full time.", 0, 0)
    match.current_seconds = 4800