import React from 'react';
import { Link, Routes, Route } from 'react-router-dom';
import Play from './Play';
import CreatePlayer from './CreatePlayer';
import Stats from './Stats';
import Settings from './Settings';

export default function PremierLayout() {
    return (
        <>
            <nav className="subnavbar">
                <Link className="subnavlink" to="play">Play</Link>
                <Link className="subnavlink" to="create-a-player">Create-A-Player</Link>
                <Link className="subnavlink" to="stats">Stats</Link>
                <Link className="subnavlink" to="settings">Settings</Link>
            </nav>

            <div className="page-content">
                <Routes>
                    <Route path="play" element={<Play />} />
                    <Route path="create-a-player" element={<CreatePlayer />} />
                    <Route path="stats" element={<Stats />} />
                    <Route path="settings" element={<Settings />} />
                </Routes>
            </div>
        </>
    );
}
