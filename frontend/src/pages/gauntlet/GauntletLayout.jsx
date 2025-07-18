import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';

export default function GauntletLayout() {
    return (
        <>
            <nav className="subnavbar">
                <Link className="subnavlink" to="team-builder">Team Builder</Link>
                <Link className="subnavlink" to="battle-history">Battle History</Link>
            </nav>

            <Routes>
                <Route path="team-builder" element={<h2>Gauntlet Team Builder</h2>} />
                <Route path="battle-history" element={<h2>Gauntlet Battle History</h2>} />
            </Routes>
        </>
    );
}
