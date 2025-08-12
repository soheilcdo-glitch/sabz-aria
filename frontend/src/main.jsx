import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import './style.css'

function App(){
  const token = localStorage.getItem("token");
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={ token ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/users" element={ token ? <Users /> : <Navigate to="/login" />} />
        <Route path="*" element={<Navigate to={ token ? "/dashboard" : "/login" } />} />
      </Routes>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App />)
