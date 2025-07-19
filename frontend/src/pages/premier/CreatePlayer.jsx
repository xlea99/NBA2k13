import React, { useState } from "react";
import "./CreatePlayer.css";

const CreatePlayer = () => {
    const [formData, setFormData] = useState({
        first: "",
        last: "",
        archetype: "Random",
        faction: "Random",
        randomAppearance: false,
        biography: "",
    });

    const rosterStats = {
        Slayer: 11,
        Vigilante: 12,
        Medic: 11,
        Guardian: 10,
        Engineer: 11,
        Director: 9,
        Total: 64,
    };

    function handleChange(e){
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === "checkbox" ? checked : value,
        });
    }

    function handleSubmit(e){
        e.preventDefault();
        console.log("Queued Player:", formData);
    }

    return (
        <main className="create-player-container">
            <h1>Create A Player</h1>
            <div className="create-player-content">
                <div className="queue-card">
                    <h2>Queue</h2>
                    <select
                        size="10"
                        className="queue-listbox"
                    >
                        {/* For now, empty. Populate with queued players later */}
                        <option disabled>(No players queued yet)</option>
                    </select>

                    <div className="queue-buttons">
                        <button className="remove-button">Remove Selected</button>
                        <button className="execute-button">Execute</button>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className="create-player-form">
                    <div className="form-group">
                        <label>First:</label>
                        <input
                            type="text"
                            name="first"
                            value={formData.first}
                            onChange={handleChange}
                            placeholder="Random"
                        />
                    </div>

                    <div className="form-group">
                        <label>Last:</label>
                        <input
                            type="text"
                            name="last"
                            value={formData.last}
                            onChange={handleChange}
                            placeholder="Random"
                        />
                    </div>

                    <div className="form-group">
                        <label>Archetype:</label>
                        <select
                            name="archetype"
                            value={formData.archetype}
                            onChange={handleChange}
                        >
                            <option>Random</option>
                            <option>Slayer</option>
                            <option>Vigilante</option>
                            <option>Medic</option>
                            <option>Guardian</option>
                            <option>Engineer</option>
                            <option>Director</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Faction:</label>
                        <select
                            name="faction"
                            value={formData.faction}
                            onChange={handleChange}
                        >
                            <option>Random</option>
                            <option>Faction A</option>
                            <option>Faction B</option>
                            <option>Faction C</option>
                        </select>
                    </div>

                    <div className="form-group checkbox-group">
                        <label>
                            <input
                                type="checkbox"
                                name="randomAppearance"
                                checked={formData.randomAppearance}
                                onChange={handleChange}
                            />
                            Random appearance
                        </label>
                    </div>

                    <div className="form-group">
                        <label>Biography:</label>
                        <textarea
                            name="biography"
                            value={formData.biography}
                            onChange={handleChange}
                            placeholder="Enter player biography here, or leave blank to randomize..."
                            rows="4"
                        ></textarea>
                    </div>

                    <button type="submit" className="queue-button">
                        Queue
                    </button>
                </form>

                <div className="roster-stats">
                    <h2>Roster Stats</h2>
                    <ul>
                        {Object.entries(rosterStats).map(([key, value]) => (
                            <li key={key}>
                                <span className="stat-label">{key}</span>{" "}
                                <span className="stat-value">{value}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </main>
    );
};

export default CreatePlayer;