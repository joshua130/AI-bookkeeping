import React from 'react'
import ReactDOM from 'react-dom/client'
import  Home from './pages/home/home.jsx'
import CompanySetup from './pages/home/companySetup/companySetup.jsx'
import { BrowserRouter, Routes, Route } from "react-router-dom";


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/company-setup" element={<CompanySetup />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
