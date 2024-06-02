
import React, { useEffect } from 'react';
import './App.css';
import { useState } from 'react';
import BasicSelect from "./components/basicSelect.tsx";
import Button from '@mui/material/Button';

interface ISquadre {
  squadra1: string;
  squadra2: string;
}

function App() {
  const [squadra1, setSquadra1] = useState("");
  const [squadra2, setSquadra2] = useState("");
  const [value, setValue] = useState<ISquadre | null>(null);

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

  const changeTeam1 = (team: string) => {
    setSquadra1(team);
  }

  const changeTeam2 = (team: string) => {
      setSquadra2(team);
  }

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
      <BasicSelect change={changeTeam1}></BasicSelect>
      <BasicSelect change={changeTeam2}></BasicSelect>
      <Button variant="outlined" onClick={handleClick}>Get winner</Button>
      {value && (
          <div>
            <p>Squadra 1: {value.squadra1}</p>
            <p>Squadra 2: {value.squadra2}</p>
          </div>
      )}
    </div>
  );
}

export default App;
