import React, { useEffect, useRef, useState } from "react";
import { Play, Pause, SkipForward, SkipBack, Volume2, Radio } from "lucide-react";
import "./RadioControls.css";

export default function RadioControls({ className = "" }) {
    const [isPlaying, setIsPlaying] = useState(false);
    const [volume, setVolume]       = useState(50);
    const [track,  setTrack]        = useState({ title: "Meep Mop", artist: "Penelope Greenbean" });
    const pollRef = useRef(null);

    function api(path, opt = {}) {
        return fetch(`http://localhost:5000/${path}`, { method: "POST", ...opt });
    }

    async function togglePlay() {
        await api(isPlaying ? "pause" : "play");
        setIsPlaying(!isPlaying);
    }

    function next()     { api("next"); }
    function prev()     { api("prev"); }
    function switchSt() { api("station/next"); }

    function changeVolume(e) {
        const v = Number(e.target.value);
        setVolume(v);
        api("volume", {
            body: JSON.stringify({ value: v }),
            headers: { "Content-Type": "application/json" },
        });
    }

    useEffect(() => {
        async function poll() {
            try {
                const s = await fetch("http://localhost:5000/status").then(r => r.json());
                setIsPlaying(s.playing);
                setVolume(s.volume);
                setTrack({ title: s.title ?? "―", artist: s.artist ?? "―" });
            } catch (_) {/* ignore unreachable server */}
        }
        poll();
        pollRef.current = setInterval(poll, 2000);
        return () => clearInterval(pollRef.current);
    }, []);

    return (
        <div className={`radio-ui ${className}`}>
            <button onClick={prev}      aria-label="Previous"><SkipBack  size={18} /></button>
            <button onClick={togglePlay} aria-label="Play / Pause">
                {isPlaying ? <Pause size={18} /> : <Play size={18} />}
            </button>
            <button onClick={next}      aria-label="Next"><SkipForward size={18} /></button>
            <button onClick={switchSt}  aria-label="Change station"><Radio size={18} /></button>

            <label className="vol">
                <Volume2 size={16} />
                <input
                    type="range"
                    min="0"
                    max="100"
                    value={volume}
                    onChange={changeVolume}
                />
            </label>

            <div className="now-playing" title={`${track.title} — ${track.artist}`}>
                {track.title} <span className="dash">—</span> {track.artist}
            </div>
        </div>
    );
}
