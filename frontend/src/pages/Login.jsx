import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { BookOpen, ArrowRight, Sparkles, Brain, Users } from 'lucide-react'
import toast from 'react-hot-toast'

const features = [
  { icon: Sparkles, t: 'AI Summaries', d: 'Turn messy notes into clear summaries' },
  { icon: Brain, t: 'Smart Quizzes', d: 'Auto-generated from your content' },
  { icon: Users, t: 'Peer Matching', d: 'Find students with shared topics' },
]

export default function Login() {
  const [isSignup, setIsSignup] = useState(false)
  const [u, setU] = useState('')
  const [p, setP] = useState('')
  const [loading, setLoading] = useState(false)
  const { login, signup } = useAuth()
  const go = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    if (!u.trim() || !p.trim()) return toast.error('Fill in all fields')
    setLoading(true)
    try {
      isSignup ? await signup(u.trim(), p) : await login(u.trim(), p)
      go('/dashboard')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Left panel */}
      <div className="hidden lg:flex lg:w-[55%] relative overflow-hidden flex-col justify-between p-12"
        style={{ background: 'linear-gradient(135deg, #4f46e5 0%, #6366f1 30%, #818cf8 70%, #a78bfa 100%)' }}>
        <div className="absolute top-20 right-20 w-72 h-72 bg-white/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-32 left-16 w-56 h-56 bg-white/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />

        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-20">
            <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-white">LearnSync</span>
          </div>
          <h2 className="text-5xl font-bold leading-tight text-white mb-6">
            Learn smarter,<br /><span className="text-indigo-200">together.</span>
          </h2>
          <p className="text-indigo-200 text-lg max-w-md">
            Upload lecture notes, get AI summaries and quizzes, connect with study partners.
          </p>
        </div>

        <div className="relative z-10 space-y-3">
          {features.map(({ icon: Icon, t, d }, i) => (
            <div key={t} className="flex items-center gap-4 p-4 rounded-2xl bg-white/10 backdrop-blur-sm border border-white/10 animate-slide-up"
              style={{ animationDelay: `${i * 150}ms` }}>
              <div className="w-10 h-10 bg-white/15 rounded-xl flex items-center justify-center">
                <Icon className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-white font-medium text-sm">{t}</p>
                <p className="text-indigo-200 text-xs">{d}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-sm animate-fade-in">
          <div className="lg:hidden flex items-center gap-3 mb-10">
            <div className="w-10 h-10 bg-brand-600 rounded-xl flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold">LearnSync</span>
          </div>

          <h2 className="text-3xl font-bold mb-2">{isSignup ? 'Get started' : 'Welcome back'}</h2>
          <p className="text-gray-400 mb-8 text-sm">{isSignup ? 'Create your account' : 'Sign in to continue'}</p>

          <form onSubmit={submit} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wider">Username</label>
              <input type="text" value={u} onChange={(e) => setU(e.target.value)} className="input-field" placeholder="Enter username" autoFocus />
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wider">Password</label>
              <input type="password" value={p} onChange={(e) => setP(e.target.value)} className="input-field" placeholder="Enter password" />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2 py-3">
              {loading
                ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                : <>{isSignup ? 'Create Account' : 'Sign In'}<ArrowRight className="w-4 h-4" /></>
              }
            </button>
          </form>

          <p className="text-center text-sm text-gray-400 mt-6">
            <button onClick={() => setIsSignup(!isSignup)} className="text-brand-600 font-medium hover:underline">
              {isSignup ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}
