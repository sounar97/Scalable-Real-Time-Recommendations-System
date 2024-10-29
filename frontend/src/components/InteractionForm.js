// InteractionForm.js
import React, { useState } from 'react';
import axios from 'axios';

function InteractionForm({ setMovieRequestId, setMusicRequestId }) {
  const [movieTitle, setMovieTitle] = useState('');
  const [artist, setArtist] = useState('');
  const [songTitle, setSongTitle] = useState('');
  const [loadingMovie, setLoadingMovie] = useState(false);
  const [loadingMusic, setLoadingMusic] = useState(false);

  const handleMovieSubmit = async (e) => {
    e.preventDefault();
    if (!movieTitle) return alert("Please enter a movie title");

    setLoadingMovie(true);
    try {
      const response = await axios.post(`http://localhost:5000/api/v1/movies/recommend`, {
        title: movieTitle,
      });
      setMovieRequestId(response.data.request_id);
    } catch (error) {
      console.error('Error fetching movie recommendations:', error);
      alert('Failed to fetch movie recommendations.');
    } finally {
      setLoadingMovie(false);
    }
  };

  const handleMusicSubmit = async (e) => {
    e.preventDefault();
    if (!artist || !songTitle) return alert("Please enter both artist and song title");

    setLoadingMusic(true);
    try {
      const response = await axios.post(`http://localhost:5000/api/v1/music/recommend`, {
        song: songTitle,
        artist,
      });
      setMusicRequestId(response.data.request_id);
    } catch (error) {
      console.error('Error fetching music recommendations:', error);
      alert('Failed to fetch music recommendations.');
    } finally {
      setLoadingMusic(false);
    }
  };

  return (
    <div className="row">
      <div className="col-md-6">
        <h3>Movie Interaction</h3>
        <form onSubmit={handleMovieSubmit}>
          <div className="mb-3">
            <label htmlFor="movieTitle" className="form-label">Movie Title</label>
            <input
              type="text"
              className="form-control"
              id="movieTitle"
              value={movieTitle}
              onChange={(e) => setMovieTitle(e.target.value)}
              placeholder="Enter movie title"
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loadingMovie}>
            {loadingMovie ? 'Loading...' : 'Get Movie Recommendations'}
          </button>
        </form>
      </div>
      <div className="col-md-6">
        <h3>Music Interaction</h3>
        <form onSubmit={handleMusicSubmit}>
          <div className="mb-3">
            <label htmlFor="artist" className="form-label">Artist</label>
            <input
              type="text"
              className="form-control"
              id="artist"
              value={artist}
              onChange={(e) => setArtist(e.target.value)}
              placeholder="Enter artist name"
            />
          </div>
          <div className="mb-3">
            <label htmlFor="songTitle" className="form-label">Song Title</label>
            <input
              type="text"
              className="form-control"
              id="songTitle"
              value={songTitle}
              onChange={(e) => setSongTitle(e.target.value)}
              placeholder="Enter song title"
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loadingMusic}>
            {loadingMusic ? 'Loading...' : 'Get Music Recommendations'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default InteractionForm;
