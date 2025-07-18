import React from 'react';
import { Link } from 'react-router-dom';
import '../app.css';
import RadioControls from './RadioControls';

export default function Navbar() {
    return (
        <nav className="navbar">
            <RadioControls className="radio-float"/>
            <Link className="navlink" to="/premier">Premier</Link>
            <Link className="navlink" to="/gauntlet">Gauntlet</Link>
            <Link className="navlink" to="/league">League</Link>
        </nav>

    );
}
