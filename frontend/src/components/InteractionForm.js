import React, { useState } from 'react';
import axios from 'axios';

function InteractionForm({ setMovieRecommendations, setMusicRecommendations }) {
  const [movieTitle, setMovieTitle] = useState('');
  const [artist, setArtist] = useState('');
  const [songTitle, setSongTitle] = useState('');

  const handleMovieSubmit = (e) => {
    e.preventDefault();
    axios.get(`http://localhost:5000/recommend/movie?title=${movieTitle}`)
      .then(response => {
        setMovieRecommendations(response.data.recommendations);
        sendInteractionToKafka({ interaction: `Viewed movie: ${movieTitle}` });
      })
      .catch(err => console.error(err));
  };

  const handleMusicSubmit = (e) => {
    e.preventDefault();
    axios.get(`http://localhost:5000/recommend/music?artist=${artist}&song=${songTitle}`)
      .then(response => {
        setMusicRecommendations(response.data.recommendations);
        sendInteractionToKafka({ interaction: `Played song: ${songTitle} by ${artist}` });
      })
      .catch(err => console.error(err));
  };

  const sendInteractionToKafka = (interactionData) => {
    axios.post('http://localhost:5000/api/track_interaction', interactionData)
      .then(response => console.log('Interaction sent to Kafka', response.data))
      .catch(err => console.error('Error sending interaction to Kafka:', err));
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
          <button type="submit" className="btn btn-primary">Get Movie Recommendations</button>
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
          <button type="submit" className="btn btn-primary">Get Music Recommendations</button>
        </form>
      </div>
    </div>
  );
}

export default InteractionForm;
