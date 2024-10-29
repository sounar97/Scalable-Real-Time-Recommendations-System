// MusicRecommendations.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function MusicRecommendations({ requestId }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!requestId) return;

    const fetchResults = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/v1/music/results/${requestId}`);
        if (response.data.recommendations) {
          setRecommendations(response.data.recommendations);
          setLoading(false);
        } else {
          setTimeout(fetchResults, 2000);  // Poll every 2 seconds if results not ready
        }
      } catch (error) {
        console.error('Error fetching music recommendations:', error);
      }
    };

    fetchResults();
  }, [requestId]);

  if (loading) {
    return <p>Loading recommendations...</p>;
  }

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
