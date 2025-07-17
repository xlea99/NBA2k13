import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import Landing from './LandingPage.jsx'
import Play from './Play';
import CreatePlayer from './CreatePlayer';
import Stats from './Stats';
import Settings from './Settings';

export default function PremierLayout() {
    return (
        <>
            <nav className="subnavbar">
                <Link className="subnavlink" to="/premier/play">Play</Link>
                <Link className="subnavlink" to="/premier/CreatePlayer">Create-A-Player</Link>
                <Link className="subnavlink" to="/premier/stats">Stats</Link>
                <Link className="subnavlink" to="/premier/settings">Settings</Link>
            </nav>

            <div className="page-content">
                <Routes>
                    <Route index element={<Landing />} />
                    <Route path="play" element={<Play />} />
                    <Route path="CreatePlayer" element={<CreatePlayer />} />
                    <Route path="stats" element={<Stats />} />
                    <Route path="settings" element={<Settings />} />
                </Routes>
            </div>
        </>
    );
}
