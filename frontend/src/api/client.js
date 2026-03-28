import axios from 'axios'

const api = axios.create({
  baseURL: window.location.hostname === 'localhost'
    ? '/api'
    : 'https://learnsync-api.onrender.com/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (e) => {
    if (e.response?.status === 401) {
      localStorage.clear()
      window.location.href = '/login'
    }
    return Promise.reject(e)
  }
)

export default api