import React from "react";


export default function Header() {
    return (
        <header className="header">
            <div className="toolbar">
                <div className="">
                    <span>Big Enquete</span>
                </div>
                <div className="">
                    <button>Login</button>
                    <span>Sign Up</span>
                </div>
            </div>
        </header>
    );
}