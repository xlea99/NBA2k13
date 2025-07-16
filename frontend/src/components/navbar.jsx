import React from 'react';
import { Link } from 'react-router-dom';
import '../app.css';

export default function Navbar() {
    return (
        <nav className="navbar">
            <Link className="navlink" to="/premier">Premier</Link>
            <Link className="navlink" to="/gauntlet">Gauntlet</Link>
            <Link className="navlink" to="/league">League</Link>
        </nav>
    );
}
