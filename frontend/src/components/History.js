import React, { useState, useEffect } from 'react';
import axios from 'axios';

const HistoryPage = () => {
  const [transportData, setTransportData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/history');
        setTransportData(response.data);
      } catch (error) {
        console.error('Error fetching transport data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Transportation Price History</h1>
      <table>
        <thead>
          <tr>
            <th>Factory Name</th>
            <th>Date</th>
            <th>Working Day</th>
            <th>Distance (KM)</th>
            <th>Petro Price per Liter (THB)</th>
            <th>Can Use Rate (THB)</th>
          </tr>
        </thead>
        <tbody>
          {transportData.map((record, index) => (
            <tr key={index}>
              <td>{record[1]}</td>
              <td>{new Date(record[5]).toLocaleString()}</td>
              <td>{record[6]}</td>
              <td>{record[2].toFixed(2)}</td>
              <td>{record[3].toFixed(2)}</td>
              <td>{record[4].toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HistoryPage;