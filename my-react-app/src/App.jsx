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

  return (
    <div className="select-company">
      <label htmlFor="company-select">Select a company:</label>
      <select id="company-select" value={selectedCompany} onChange={(e) => setSelectedCompany(e.target.value)}>
        <option value="">--Please choose an option--</option>
        {companies.map((company) => (
          <option key={company.id} value={company.id}>
            {company.name}
          </option>
        ))}
      </select>
    </div>
  );
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