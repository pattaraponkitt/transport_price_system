import React from 'react';

const ResultPage = ({ data }) => {
  // Destructure the necessary data from props
  const { factory, distance, petroPrice } = data;

  return (
    <div>
      {/* Render the result data */}
      <h2>Factory Name: {factory.toUpperCase()}</h2>
      <p>Distance: {distance.toFixed(2)} KM</p>
      <p>Petro Price per Liter: {petroPrice.toFixed(2)} THB</p>
      {/* Render the remaining result data */}
    </div>
  );
};

export default ResultPage;