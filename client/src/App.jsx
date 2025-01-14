import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import StockDetail from './components/StockDetail';

const App = () => {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/stock/:stock" element={<StockDetail />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
