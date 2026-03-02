import React, {useState} from 'react'
import {useHistory} from 'react-router-dom'
import axios from 'axios'

const Login = ()=> {

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState(null)
    const history = useHistory()

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            response = await axios.post('http://localhost:8004/api/v1/auth/login', {username, password})
            // sor token 
            history.push('/home')
        } catch (err) {
            setError('Login failed. Please check your credentials and try again.')
        }
    }

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;