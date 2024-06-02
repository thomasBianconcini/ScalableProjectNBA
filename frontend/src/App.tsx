
import React, { useEffect } from 'react';
import './App.css';
import { useState } from 'react';
import BasicSelect from "./components/basicSelect.tsx";
import ButtonAppBar from "./components/appBar.tsx";
import Button from '@mui/material/Button';
import {Grid} from "@mui/material";
import Typography from '@mui/material/Typography';
import background from './wallpaperone.jpg';

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
    <div className="App" style={{backgroundImage: `url(${background})`, backgroundSize: 'cover', height:'100vh'}}>
      <ButtonAppBar></ButtonAppBar>
      <Grid container spacing={2} paddingTop={10} paddingLeft={10} paddingRight={10}>
        <Grid item xs={4}></Grid>
        <Grid item xs={8}>
          <Typography variant="h2">Choose teams</Typography>
        </Grid>
        <Grid item xs={4}></Grid>
        <Grid item xs={4}>
          <BasicSelect change={changeTeam1}></BasicSelect>
        </Grid>
        <Grid item xs={4}>
          <BasicSelect change={changeTeam2}></BasicSelect>
        </Grid>
        <Grid item xs={4}></Grid>
        <Grid item xs={8}>
          <Button variant="outlined" onClick={handleClick}>Get winner</Button>
        </Grid>
        <Grid item xs={4}></Grid>
        <Grid item xs={8}>
          {value && (
              <div>
                <p>Squadra 1: {value.squadra1}</p>
                <p>Squadra 2: {value.squadra2}</p>
              </div>
          )}
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
