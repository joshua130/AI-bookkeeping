import React from "react";
import { Header } from "../../../components/layout/header";
import { Button } from "../../../components/layout/button";
import "./companySetup.css";
import { useNavigate } from "react-router-dom";

function CompanySetup() {
    const navigate = useNavigate();
    const [code, setCode] = React.useState("");
    const [name, setName] = React.useState("");

    const isValidCode = (val) => /^\d{3}$/.test(val);
    const isInvalid = !isValidCode(code) || name.trim().length === 0;

    return(
        <div>
            <div className="setup-header">
                <div style={{ position: "relative"}}>
                    <Header label="AI-Bookkeeping" />
                </div>
                <div style={{ position: "absolute", right: "20px" ,top: "8px" ,}}>
                    <Button label="ホーム" onClick={() => navigate("/")} color="white" fontSize={"13px"} width="100px" height="30px"   />
                </div>
            </div>
            <main>
                <div>
                    /*以下は仮*/
                    <form action="http://localhost:5000/setUp/postAccountItem" method="post" enctype="multipart/form-data">
                        <h3>3桁の会社コードを入力してください</h3>
                            <input type="text" value={code} onChange={(e) => setCode(e.target.value)} maxLength={3} placeholder="会社コード" className="companyCodeInput" name="code"/>
                        <h3>会社名を入力してください</h3>
                            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="会社名" className="companyNameInput" name="name"/>
                        <input type="file" name="file" />
                        <button type="submit" disabled={isInvalid}>アップロード</button>
                    </form>
                </div>
            </main>
        </div>
    );
}      

export default CompanySetup;