import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';

export default function LeagueLayout() {
    return (
        <>
            <nav className="subnavbar">
                <Link className="subnavlink" to="season-schedule">Season Schedule</Link>
                <Link className="subnavlink" to="standings">Standings</Link>
                <Link className="subnavlink" to="trades">Trades</Link>
                <Link className="subnavlink" to="player-stats">Player Stats</Link>
            </nav>

            <Routes>
                <Route path="season-schedule" element={<h2>League Season Schedule</h2>} />
                <Route path="standings" element={<h2>League Standings</h2>} />
                <Route path="trades" element={<h2>League Trades</h2>} />
                <Route path="player-stats" element={<h2>League Player Stats</h2>} />
            </Routes>
        </>
    );
}
