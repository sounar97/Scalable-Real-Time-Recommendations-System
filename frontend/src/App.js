import React, { useState } from 'react';
import InteractionForm from './components/InteractionForm';
import MovieRecommendations from './components/MovieRecommendations';
import MusicRecommendations from './components/MusicRecommendations';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [movieRecommendations, setMovieRecommendations] = useState([]);
  const [musicRecommendations, setMusicRecommendations] = useState([]);

  return (
    <div className="container mt-4">
      <h1 className="text-center">Real-Time Recommendation System</h1>
      <InteractionForm
        setMovieRecommendations={setMovieRecommendations}
        setMusicRecommendations={setMusicRecommendations}
      />
      <div className="row mt-4">
        <div className="col-md-6">
          <MovieRecommendations recommendations={movieRecommendations} />
        </div>
        <div className="col-md-6">
          <MusicRecommendations recommendations={musicRecommendations} />
        </div>
      </div>
    </div>
  );
}

export default App;
