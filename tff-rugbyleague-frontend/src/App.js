import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Make sure to import the CSS file
import team1 from './team1';
import team2 from './team2';

function App() {
  const [commentary, setCommentary] = useState([]);
  const [matchStarted, setMatchStarted] = useState(false);
  const [matchPaused, setMatchPaused] = useState(true);
  const [matchState, setMatchState] = useState({
    team1: team1,
    team2: team2,
    team1_state: {},
    team2_state: {},
    current_seconds: 0,
  });

  useEffect(() => {
    let interval;
    if (matchStarted && !matchPaused) {
      interval = setInterval(fetchMatchState, 2000); // Fetch match state every 2 seconds
    }
    return () => clearInterval(interval); // Cleanup on component unmount or when matchStarted/matchPaused changes
  }, [matchStarted, matchPaused]);

  const fetchMatchState = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/get-match-state');
      setMatchState(prevState => ({
        ...prevState,
        team1_score: response.data.team1_score,
        team2_score: response.data.team2_score,
        team1_state: response.data.team1_state,
        team2_state: response.data.team2_state,
        current_seconds: response.data.current_seconds,
        current_tackle_count: response.data.current_tackle_count,
        current_team_possession: response.data.current_team_possession,
        current_position_x: response.data.current_position_x,
        current_position_y: response.data.current_position_y,
      }));
      setMatchPaused(response.data.paused);
      setCommentary(response.data.commentary);
    } catch (error) {
      console.error("Error fetching match state:", error);
    }
  };

  const handleStartGame = async () => {
    setMatchStarted(true);
    setMatchPaused(false);
    try {
      const response = await axios.post('http://127.0.0.1:5000/start-game', {
        team1: matchState.team1,
        team2: matchState.team2,
      });
      setCommentary(response.data.commentary);
    } catch (error) {
      console.error("Error starting the game:", error);
    }
  };

  const togglePauseGame = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/pause-game', {
        team1: matchState.team1,
        team2: matchState.team2,
      });
      setMatchPaused(response.data.paused);
    } catch (error) {
      console.error("Error toggling game pause:", error);
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = (seconds % 60).toFixed(0);
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Rugby League Simulator</h1>
        <div className="scoreboard">
          <div
            className="team-1"
            style={{
              backgroundColor: matchState.team1.primaryColour,
              color: matchState.team1.secondaryColour,
            }}
          >
            {matchState.team1.name} <div className="score">{matchState.team1_score ?? "-"}</div>
          </div>
          <div
            className="team-2"
            style={{
              backgroundColor: matchState.team2.primaryColour,
              color: matchState.team2.secondaryColour,
            }}
          >
            {matchState.team2.name} <div className="score">{matchState.team2_score ?? "-"}</div>
          </div>
        </div>
        <div className="timer">{formatTime(matchState.current_seconds)}</div>
        <br />
        <div className="tackle-count">
          <div>{`Tackle ${matchState.current_tackle_count ?? 0}`}</div>
        </div>
        <br />
        <div
          className="live-commentary"
          style={{
            backgroundColor:
              matchState.current_team_possession === 1
                ? matchState.team1.primaryColour
                : matchState.team2.primaryColour,
            color:
              matchState.current_team_possession === 1
                ? matchState.team1.secondaryColour
                : matchState.team2.secondaryColour,
          }}
        >
          {commentary.length > 0
            ? commentary[commentary.length - 1]
            : `${matchState.team1.name} - ${matchState.team2.name} kicks off soon.`}
        </div>
        <div className="pitch-radar">
          <div className="pitch-radar-line ingoal-left" />
          <div className="pitch-radar-line ingoal-right" />
          <div className="pitch-radar-line tryline-left" />
          <div className="pitch-radar-line tryline-right" />
          <div className="pitch-radar-line tenline-left" />
          <div className="pitch-radar-line tenline-right" />
          <div className="pitch-radar-line twentyline-left" />
          <div className="pitch-radar-line twentyline-right" />
          <div className="pitch-radar-line thirtyline-left" />
          <div className="pitch-radar-line thirtyline-right" />
          <div className="pitch-radar-line fortyline-left" />
          <div className="pitch-radar-line fortyline-right" />
          <div className="pitch-radar-line half-way" />
          <div className="pitch-radar-line touchline-bottom" />
          <div className="pitch-radar-line touchline-top" />
          <div
            className="pitch-radar-ball"
            style={{
              top: (matchState.current_position_x * 2) + 5 || 75,
              left: (matchState.current_position_y * 5) + 15 || 315,
              backgroundColor:
                matchState.current_team_possession === 1
                  ? matchState.team1.primaryColour
                  : matchState.team2.primaryColour,
            }}
          />
        </div>
        <button
          className={`action-button ${matchStarted ? 'disabled' : ''}`}
          onClick={handleStartGame}
          disabled={matchStarted}
        >
          {matchStarted ? "Game Started" : "Start Game"}
        </button>
        {matchStarted && (
          <button className="action-button" onClick={togglePauseGame}>
            {matchPaused ? "Continue Game" : "Pause Game"}
          </button>
        )}
      </div>
      <div className="content">
        <div
          className="team-column"
          style={{
            backgroundColor: matchState.team1.primaryColour,
            color: matchState.team1.secondaryColour,
          }}
        >
          {Object.entries(matchState.team1_state).map(([id, state]) => (
            <p className={state.interchange ? "interchange" : ""} key={id}>
              {state.name}: {(state.rating / 10).toFixed(1)}
            </p>
          ))}
        </div>
        <div className="commentary-column">
          <h3>Match Report</h3>
          {commentary.slice(0).reverse().map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
        <div
          className="team-column"
          style={{
            backgroundColor: matchState.team2.primaryColour,
            color: matchState.team2.secondaryColour,
          }}
        >
          {Object.entries(matchState.team2_state).map(([id, state]) => (
            <p className={state.interchange ? "interchange" : ""} key={id}>
              {state.name}: {(state.rating / 10).toFixed(1)}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
