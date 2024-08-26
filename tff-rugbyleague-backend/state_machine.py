from collections import deque

class MatchStateMachine:
    def __init__(self, match):
        self.match = match
        self.state = KickoffState(match)  # Start with the kickoff state
        self.event_queue = deque()  # Initialise the event queue
        self.paused = False  # Add a paused state to control game flow

    def queue_event(self, event):
        """Add an event to the event queue."""
        self.event_queue.append(event)

    def run(self):
        """Main loop to process the event queue."""
        while self.event_queue:
            if self.paused:
                # If the game is paused, skip processing
                continue
            event = self.event_queue.popleft()  # Get the next event
            self.state = self.state.handle_event(event)  # Transition to the next state
            self.state.on_enter()  # Execute the logic for the new state

    def start(self):
        """Start the match."""
        self.state.on_enter()

    def toggle_pause(self):
        """Toggle the paused state."""
        self.paused = not self.paused
        if isinstance(self.state, HalfTimeState) and not self.paused:
            self.state = KickoffState(self.match)
            from events.kick_off import kick_off
            result = kick_off(self.match)
            self.event_queue.append(result)
            self.run()
        return self.paused

class State:
    def __init__(self, match, **kwargs):
        self.match = match
        self.context = kwargs

    def on_enter(self):
        """Logic when entering a state."""
        pass

    def handle_event(self, event):
        """Handle an event and possibly transition to another state."""
        pass


class KickoffState(State):
    def on_enter(self):
        from events.kick_off import kick_off
        result = kick_off(self.match)
        self.match.state_machine.queue_event(result)

    def handle_event(self, event):
        if event["event"] == "kicked_off":
            return PlayState(self.match, event="catch_kick", kicker=event["kicker"], kick_type=event["kick_type"], kick_distance=event["kick_distance"])
        elif event["event"] == "out_on_full":
            return PenaltyState(self.match, event="penalty")
        return self
    

class HalfTimeState(State):
    def on_enter(self):
        from events.half_time import half_time
        half_time(self.match)
        self.match.state_machine.toggle_pause()

class FullTimeState(State):
    def on_enter(self):
        from events.full_time import full_time
        full_time(self.match)
        self.paused = True


class PlayState(State):
    def __init__(self, match, event, **kwargs):
        super().__init__(match, **kwargs)
        self.event = event

    def on_enter(self):
        result = None

        if self.event == "bomb_kick":
            from events.bomb_kick import bomb_kick
            kicker = self.context.get("kicker")
            result = bomb_kick(self.match, kicker)

        elif self.event == "carry_ball":
            from events.meet_defence import meet_defence
            ball_carrier = self.context.get("ball_carrier")
            tackler = self.context.get("tackler")
            defence_distance = self.context.get("defence_distance")
            result = meet_defence(self.match, ball_carrier, tackler, defence_distance)

        elif self.event == "catch_kick":
            from events.catch_kick import catch_kick
            kicker = self.context.get("kicker")
            kick_type = self.context.get("kick_type")
            kick_distance = self.context.get("kick_distance")
            kick_height = self.context.get("kick_height")
            result = catch_kick(self.match, kicker, kick_type, kick_distance, kick_height)

        elif self.event == "drop_out":
            from events.drop_out import drop_out
            result = drop_out(self.match)

        elif self.event == "dummy_half":
            from events.dummy_half import dummy_half
            ball_player = self.context.get("ball_player")
            result = dummy_half(self.match, ball_player)

        elif self.event == "line_break":
            from events.line_break import line_break
            ball_carrier = self.context.get("ball_carrier")
            result = line_break(self.match, ball_carrier)

        elif self.event == "long_kick":
            from events.long_kick import long_kick
            kicker = self.context.get("kicker")
            result = long_kick(self.match, kicker)

        elif self.event == "pass_ball":
            from events.pass_ball import pass_ball
            passer = self.context.get("passer")
            target = self.context.get("target")
            next_play = self.context.get("next_play")
            result = pass_ball(self.match, passer, target, next_play)

        elif self.event == "short_kick":
            from events.short_kick import short_kick
            kicker = self.context.get("kicker")
            ball_player = self.context.get("ball_player")
            result = short_kick(self.match, kicker, ball_player)

        elif self.event == "tackle":
            from events.attempt_tackle import attempt_tackle
            ball_carrier = self.context.get("ball_carrier")
            tackler = self.context.get("tackler")
            result = attempt_tackle(self.match, ball_carrier, tackler)

        elif self.event == "turnover":
            from events.turnover import turnover
            result = turnover(self.match)
        
        if result:
            self.match.state_machine.queue_event(result)

    def handle_event(self, event):
        if event["event"] == "bomb_kick":
            return PlayState(self.match, event="bomb_kick", kicker=event["kicker"])
        elif event["event"] == "catch_kick":
            return PlayState(self.match, event="catch_kick", kicker=event["kicker"], kick_type=event["kick_type"], kick_distance=event["kick_distance"], kick_height=event["kick_height"])
        elif event["event"] == "caught_kick":
            return PlayState(self.match, event="carry_ball", ball_carrier=event["ball_carrier"], tackler=event["tackler"], defence_distance=event["defence_distance"])
        elif event["event"] == "dropped_kick":
            return ScrumState(self.match)
        elif event["event"] == "drop_out":
            return PlayState(self.match, event="drop_out")
        elif event["event"] == "dummy_half":
            return PlayState(self.match, event="dummy_half", ball_player=event["ball_player"])
        elif event["event"] == "full_time":
            return FullTimeState(self.match)
        elif event["event"] == "half_time":
            return HalfTimeState(self.match)
        elif event["event"] == "knock_on":
            return ScrumState(self.match)
        elif event["event"] == "line_break":
            return PlayState(self.match, event="line_break", ball_carrier=event["ball_carrier"])
        elif event["event"] == "long_kick":
            return PlayState(self.match, event="long_kick", kicker=event["kicker"])
        elif event["event"] == "pass_ball":
            return PlayState(self.match, event="pass_ball", passer=event["passer"], target=event["target"], next_play=event["next_play"])
        elif event["event"] == "penalty":
            return PenaltyState(self.match, event="penalty")
        elif event["event"] == "short_kick":
            return PlayState(self.match, event="short_kick", kicker=event["kicker"], ball_player=event["ball_player"])
        elif event["event"] == "tackled":
            return PlayState(self.match, event="tackle", ball_carrier=event["ball_carrier"], tackler=event["tackler"])
        elif event["event"] == "try_scored":
            return TryState(self.match, event="try_scored")
        elif event["event"] == "turnover":
            return PlayState(self.match, event="turnover")

        return self


class PenaltyState(State):
    def __init__(self, match, event, **kwargs):
        super().__init__(match, **kwargs)
        self.event = event

    def on_enter(self):
        if self.event == "kick_to_touch":
            from events.kick_to_touch import kick_to_touch
            result = kick_to_touch(self.match)
        elif self.event == "penalty_kick":
            from events.penalty_kick import penalty_kick
            result = penalty_kick(self.match)
        else:
            from events.penalty import penalty
            result = penalty(self.match)

        self.match.state_machine.queue_event(result)

    def handle_event(self, event):
        if event["event"] == "drop_out":
            return PlayState(self.match, event="drop_out")
        elif event["event"] == "dummy_half":
            return PlayState(self.match, event="dummy_half", ball_player=event["ball_player"])
        elif event["event"] == "full_time":
            return FullTimeState(self.match)
        elif event["event"] == "half_time":
            return HalfTimeState(self.match)
        elif event["event"] == "kick_off":
            return KickoffState(self.match)
        elif event["event"] == "kick_to_touch":
            return PenaltyState(self.match, event="kick_to_touch")
        elif event["event"] == "penalty_kick":
            return PenaltyState(self.match, event="penalty_kick")
        return self


class ScrumState(State):
    def on_enter(self):
        from events.scrum import scrum
        result = scrum(self.match)
        if result:
            self.match.state_machine.queue_event(result)

    def handle_event(self, event):
        if event["event"] == "full_time":
            return FullTimeState(self.match)
        elif event["event"] == "half_time":
            return HalfTimeState(self.match)
        elif event["event"] == "pass_ball":
            return PlayState(self.match, event="pass_ball", passer=event["passer"], target=event["target"], next_play=event["next_play"])
        elif event["event"] == "penalty":
            return PenaltyState(self.match, event="penalty")
        return self
    

class TryState(State):
    def __init__(self, match, event, **kwargs):
        super().__init__(match, **kwargs)
        self.event = event
    
    def on_enter(self):
        if self.event == "conversion_kick":
            from events.conversion_kick import conversion_kick
            result = conversion_kick(self.match)
        else:
            from events.try_score import try_score
            result = try_score(self.match)
        
        if result:
            self.match.state_machine.queue_event(result)

    def handle_event(self, event):
        if event["event"] == "conversion_kick":
            return TryState(self.match, event="conversion_kick")
        elif event["event"] == "full_time":
            return FullTimeState(self.match)
        elif event["event"] == "half_time":
            return HalfTimeState(self.match)
        elif event["event"] == "kick_off":
            return KickoffState(self.match)
        return self
