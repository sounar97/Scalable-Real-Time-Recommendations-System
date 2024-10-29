import React, { useState } from 'react';
import InteractionForm from './components/InteractionForm';
import MovieRecommendations from './components/MovieRecommendations';
import MusicRecommendations from './components/MusicRecommendations';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [movieRequestId, setMovieRequestId] = useState(null);
  const [musicRequestId, setMusicRequestId] = useState(null);
  return (
    <div className="container mt-4">
      <h1 className="text-center">Real-Time Recommendation System</h1>
      <InteractionForm
        setMovieRequestId={setMovieRequestId}
        setMusicRequestId={setMusicRequestId}
      />
      <div className="row mt-4">
        <div className="col-md-6">
        {movieRequestId && <MovieRecommendations requestId={movieRequestId} />}
        </div>
        <div className="col-md-6">
        {musicRequestId && <MusicRecommendations requestId={musicRequestId} />}
        </div>
      </div>
    </div>
  );
}

export default App;

