import './App.css';
import React,{ useEffect, useState} from 'react';

function header() {
  return (
    <header>
      <h1 className="header">AI-Bookkeeping</h1>
    </header>
  );
}

function select_company() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/companies/');
        const data = await response.json();
        setCompanies(data);
      } catch (error) {
        console.error('Error fetching companies:', error);
      }
    };

    fetchCompanies();
  }, []);

  return ();
}

function App() {
  return (
    <div className="App">
      {header()}
      {select_company()}
    </div>
  );
}
export default App;