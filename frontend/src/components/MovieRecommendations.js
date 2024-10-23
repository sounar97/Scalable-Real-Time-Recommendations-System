import React from 'react';

function MovieRecommendations({ recommendations }) {
  return (
    <div>
      <h3>Movie Recommendations</h3>
      <ul className="list-group">
        {recommendations.map((movie, index) => (
          <li key={index} className="list-group-item">
            {movie}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MovieRecommendations;
