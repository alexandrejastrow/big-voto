import React from "react";

import Header from "./components/Header";
import './style.css'

export default function Home() {
    return (
        <div>
            <Header />
            <main className="main">
                <div className="navbar">nav</div>
                <div className="feed">feed</div>
            </main>
        </div>
    );
}
