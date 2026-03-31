import React from "react";
import { Header } from "../../../components/layout/header";
import { Button } from "../../../components/layout/button";
import "./companySetup.css";
import { useNavigate } from "react-router-dom";

function CompanySetup() {
    const navigate = useNavigate();

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
                <div className="companySetup-main">
                    <h3>3桁の会社コードを入力してください</h3>
                    <input type="text" placeholder="会社コード" className="companyCodeInput" name="code"/>
                    <h3>会社名を入力してください</h3>
                    <input type="text" placeholder="会社名" className="companyNameInput" name="name"/>
                </div>
                <div>
                    /*以下は仮*/
                    <form action="http://localhost:5000/setUp/postAccountItem" method="post" encType="multipart/form-data">
                        <input type="file" name="file" />
                        <button type="submit">アップロード</button>
                    </form>
                </div>
            </main>
        </div>
    );
}      

export default CompanySetup;