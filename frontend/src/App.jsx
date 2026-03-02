import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Home from "./pages/Rome"
import Login from "./pages/Login"

// import Register from "./pages/Register"

function PrivateRoute({ children}) {
    const token = localStorage.getItem("access_token")
    return token ? children : <Navigate to="/login" />;
}

function App() {
    return (
        <Router>
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<PrivateRoute>
                <Home />
                </PrivateRoute>
            }
        />
        </Routes>
        </Router>
    )   

}

export default App;
