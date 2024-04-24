import React, { useState } from 'react';
import axios from 'axios';
import ResultPage from './Result';

const MainForm = () => {
  const [factory, setFactory] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [resultData, setResultData] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const formData = {
        factory,
        // Add other form data here
      };

      const response = await axios.post('/api/calculate', formData);
      setResultData(response.data);
      setShowResult(true);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <div>
      {showResult ? (
        <ResultPage data={resultData} />
      ) : (
        <form onSubmit={handleSubmit}>
          {/* Render the form fields */}
          <input
            type="text"
            name="factory"
            id="factory"
            value={factory}
            onChange={(e) => setFactory(e.target.value)}
            required
          />
          {/* Add the remaining form fields */}
          <input type="submit" value="Calculate" />
        </form>
      )}
    </div>
  );
};

export default MainForm;