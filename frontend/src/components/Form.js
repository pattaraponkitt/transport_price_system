import React, { useState } from 'react';
import './Form.css';

const Form = () => {
  const [factory, setFactory] = useState('');
  const [distance, setDistance] = useState('');
  const [petroPrice, setPetroPrice] = useState('');
  const [workingDay, setWorkingDay] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  const validateForm = () => {
    if (
      distance === '' ||
      petroPrice === '' ||
      workingDay === '' ||
      distance <= 0 ||
      petroPrice <= 0 ||
      workingDay <= 0
    ) {
      alert('Please enter valid values for distance, petro price, and working day.');
      return false;
    }
    return true;
  };

  return (
    <div>
      <h1>TRANSPORT STANDARD PRICE SYSTEM</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="factory">Factory Name:</label>
        <input
          type="text"
          id="factory"
          value={factory}
          onChange={(e) => setFactory(e.target.value)}
          required
        />
        <br />
        <br />

        <label htmlFor="distance">Distance:</label>
        <input
          type="number"
          id="distance"
          step="0.01"
          value={distance}
          onChange={(e) => setDistance(e.target.value)}
          required
        />
        <br />
        <br />

        <label htmlFor="petro_price">Petro Price per Liter:</label>
        <input
          type="number"
          id="petro_price"
          step="0.01"
          value={petroPrice}
          onChange={(e) => setPetroPrice(e.target.value)}
          required
        />
        <br />
        <br />

        <label htmlFor="day">Working Day:</label>
        <input
          type="number"
          id="day"
          value={workingDay}
          onChange={(e) => setWorkingDay(e.target.value)}
          required
        />
        <br />
        <br />

        <input
          type="submit"
          value="Calculate"
          onClick={() => validateForm()}
        />
      </form>
    </div>
  );
};

export default Form;