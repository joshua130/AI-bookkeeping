import React,{useState,useEffect} from "react";
import { Header } from "../../components/layout/header";
import "./home.css";
import { Button } from "../../components/layout/button";
import { Selecter } from "../../components/layout/selecter";
import { useNavigate } from "react-router-dom";

function Home() {
    const navigate = useNavigate();
    const { companies, selectedCompany, setSelectedCompany } = useCompanySelect();
    return(
        <div>
            <div className="home-header">
                <div style={{ position: "relative"}}>
                    <Header label="AI-Bookkeeping" />
                </div>
                <div style={{ position: "absolute", right: "20px" ,top: "8px" ,}}>
                    <Button label="セットアップ" onClick={() => navigate("/company-setup")} color="white" fontSize={"13px"} width="100px" height="30px"   />
                </div>
            </div>

            <main>
                <div className="companySelector">
                    <div id="Selector">
                        <Selecter options={[
                            {value: "", label: "会社を選択してください"},
                            ...companies.map((company) => ({
                                value: company.id,
                                label: company.id,
                            }))]
                        } onChange={(e) => {
                            const id = e.target.value;
                            const company =companies.find((c) => String(c.id) === String(id));
                            setSelectedCompany(company);
                        }} />
                    </div>
                    <div id = "companyName">
                        {selectedCompany ? selectedCompany.name : ""}
                    </div>
                </div>
                <div>    
                
                </div>     

            </main>  
        </div>
    );
};

function useCompanySelect() {
    const [companies, setCompanies] = useState([]);
    const [selectedCompany, setSelectedCompany] = useState("");

    useEffect(() => {
        const fetchCompanies = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/get_company');
                const data = await response.json();
                setCompanies(data);
            } catch (error) {
                console.error('Error fetching companies:', error);
            }
        };

        fetchCompanies();
    }, []);

    return { companies, selectedCompany, setSelectedCompany };
}

export default Home;
