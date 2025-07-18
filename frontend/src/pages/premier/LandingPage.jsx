import React, { useEffect, useRef } from "react";
import "./LandingPage.css";

export default function LandingPage() {
    const audioRef = useRef(null);

    useEffect(() => {
        const audio = new Audio("/SodaCityFunk.mp3");
        audio.loop = true;
        audio.volume = 0.4;
        audioRef.current = audio;

        const tryPlay = () => audio.play().catch(() => {});
        tryPlay();

        const resumeOnInteraction = () => {
            tryPlay();
            document.removeEventListener("pointerup", resumeOnInteraction);
            document.removeEventListener("keydown", resumeOnInteraction);
        };

        document.addEventListener("pointerup", resumeOnInteraction, { once: true });
        document.addEventListener("keydown", resumeOnInteraction,   { once: true });

        return () => {
            audio.pause();
            audio.currentTime = 0;
            document.removeEventListener("pointerup", resumeOnInteraction);
            document.removeEventListener("keydown", resumeOnInteraction);
        };
    }, []);

    return (
        <div className="landing-row">            {/* keep .landing-row position: relative in CSS */}
            <div className="landing-text">
                <h2 className="premier-welcome bass-drop">
          <span className="fade delay-1">
            Welcome to <span className="underline delay-1">Premier</span>.
          </span>
                    <br />
                    <span className="fade delay-2">
            It&apos;s time to game with the <span className="underline delay-2">best</span>.
          </span>
                    <br />
                    <span className="fade delay-3">
            Select a mode on the menu above to begin.
          </span>
                </h2>
            </div>

            <img
                className="lebron-img"
                src="/lebronClear.png"
                alt="Lebron James"
            />
        </div>
    );
}
