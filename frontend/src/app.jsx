import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar.jsx';
import PremierLayout from './pages/premier/PremierLayout';
import GauntletLayout from './pages/gauntlet/GauntletLayout';
import LeagueLayout from './pages/league/LeagueLayout';
import NotFound from './pages/NotFound';
import { Navigate } from "react-router-dom";
import './app.css';

function App() {
    return (
        <Router>
            <Navbar />
            <div style={{ padding: '80px 20px 20px 20px' }}>
                <Routes>
                    <Route path="/" element={<Navigate to="/premier" replace />} />
                    <Route path="/premier/*" element={<PremierLayout />} />
                    <Route path="/gauntlet/*" element={<GauntletLayout />} />
                    <Route path="/league/*" element={<LeagueLayout />} />
                    <Route path="*" element={<NotFound />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
