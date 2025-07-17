import React, { useEffect, useRef } from "react";
import "./LandingPage.css";

export default function LandingPage() {
    const audioRef = useRef(null);

    useEffect(() => {
        // 1️⃣  build the Audio element
        const audio = new Audio("/SodaCityFunk.mp3"); // file in /public
        audio.loop = true;
        audio.volume = 0.4;
        audioRef.current = audio;

        // Helper to attempt play (may fail until user interacts)
        const tryPlay = () => audio.play().catch(() => {/* ignore */});

        // 2️⃣  first attempt immediately
        tryPlay();

        // 3️⃣  if blocked, resume after any user gesture
        const resumeOnInteraction = () => {
            tryPlay();                                   // try again
            // one-shot cleanup
            document.removeEventListener("pointerup", resumeOnInteraction);
            document.removeEventListener("keydown", resumeOnInteraction);
        };

        // pointerup works for mouse + touch; keydown covers keyboard
        document.addEventListener("pointerup", resumeOnInteraction, { once: true });
        document.addEventListener("keydown", resumeOnInteraction,   { once: true });

        // 4️⃣  stop music when component unmounts
        return () => {
            audio.pause();
            audio.currentTime = 0;
            document.removeEventListener("pointerup", resumeOnInteraction);
            document.removeEventListener("keydown", resumeOnInteraction);
        };
    }, []);

    return (
        <div className="landing-row">
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
        </div>
    );
}
