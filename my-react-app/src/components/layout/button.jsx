import React from "react";

export const Button = ({ label, onClick, color = "skyblue",fontSize,width,height}) => {
    const buttonStyle = {
        backgroundColor: color,
        border: "black solid 1px",
        borderRadius: "4px",
        color: "black",
        width: width ,
        height: height,
        fontSize: fontSize,
        cursor: "pointer",
    };

    return (
        <button style={buttonStyle} onClick={onClick} fontSize="16px" width="100px" height="30px"   >
            {label}
        </button>
    );
}