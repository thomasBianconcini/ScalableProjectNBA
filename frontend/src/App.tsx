
import React, { useEffect } from 'react';
import './App.css';
import { useState } from 'react';
import axios from 'axios';

interface ISquadre {
  squadra1: string;
  squadra2: string;
}

function App() {
  const [squadra1, setSquadra1] = useState("");
  const [squadra2, setSquadra2] = useState("");
  const [value, setValue] = useState<ISquadre | null>(null);
  const [scoreboard, setScoreboard] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/scoreboard',{method:'GET', redirect: 'follow'})
    .then(response => response.text())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }, []);

  const handleClick = () => {
    const apiUrl = `http://localhost:5000/api/predict?squadra1=${squadra1}&squadra2=${squadra2}`;
    const apiKey = 'taylor';
    fetch(apiUrl, {
      method: 'GET',
      headers: {
        'X-API-KEY': apiKey
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      setValue(data);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <input
          type="text"
          value={squadra1}
          onChange={(e) => setSquadra1(e.target.value)}
          placeholder="Enter squadra1"
        />
        <input
          type="text"
          value={squadra2}
          onChange={(e) => setSquadra2(e.target.value)}
          placeholder="Enter squadra2"
        />
        <button onClick={handleClick}>Click me</button>
        {value && (
          <div>
            <p>Squadra 1: {value.squadra1}</p>
            <p>Squadra 2: {value.squadra2}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
