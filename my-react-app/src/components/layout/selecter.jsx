
export const Selecter = ({ options, onChange}) => {
    const selectStyle = {
        backgroundColor: "white",
        border: "black solid 1px",
        borderRadius: "4px",
        color : "black",

    }
    return (
        <div>
            <select onChange={onChange} style={selectStyle}>
                {options.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                        {opt.label}
                    </option>
                ))}
            </select>
        </div>
    );    
}