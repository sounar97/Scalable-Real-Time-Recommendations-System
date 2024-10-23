import React from 'react';

function MusicRecommendations({ recommendations }) {
  return (
    <div>
      <h3>Music Recommendations</h3>
      <ul className="list-group">
        {recommendations.map((song, index) => (
          <li key={index} className="list-group-item">
            {song}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MusicRecommendations;
