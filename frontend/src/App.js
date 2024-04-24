import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
//import MainForm from './components/MainForm';
import HistoryPage from './components/History';
import Form from './components/Form';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Form />} />
        <Route path="/history" element={<HistoryPage />} />
      </Routes>
    </Router>
  );
}

export default App;