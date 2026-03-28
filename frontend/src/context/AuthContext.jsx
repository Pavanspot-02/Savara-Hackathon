import { createContext, useContext, useState } from 'react'
import api from '../api/client'
import toast from 'react-hot-toast'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [username, setUsername] = useState(localStorage.getItem('username') || '')

  const auth = async (endpoint, u, p) => {
    const r = await api.post(endpoint, { username: u, password: p })
    localStorage.setItem('token', r.data.access_token)
    localStorage.setItem('username', u)
    setToken(r.data.access_token)
    setUsername(u)
    return r.data.access_token
  }

  const login = (u, p) => auth('/auth/login', u, p).then(() => toast.success('Welcome back!'))
  const signup = (u, p) => auth('/auth/signup', u, p).then(() => toast.success('Account created!'))
  const logout = () => { localStorage.clear(); setToken(null); setUsername('') }

  return (
    <AuthContext.Provider value={{ token, username, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
