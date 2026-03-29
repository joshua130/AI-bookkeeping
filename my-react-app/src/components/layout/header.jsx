import React from 'react';


export const Header = ({label,color = "RoyalBlue"}) => {
    const headerStyle = {
        backgroundColor: color,
    };

    return (
        <header style={headerStyle}>
            <h1 style={{
                position: "relative",
                fontFamily: "Arial, sans-serif",
                fontSize: "24px",
                color: "white",
                textAlign: "left",
                padding: "10px",
                margin: "0",
            }}>{label}</h1>
        </header>
    );
};    

