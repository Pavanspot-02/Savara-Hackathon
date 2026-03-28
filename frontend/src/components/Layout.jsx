import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { LayoutDashboard, Upload, Brain, Users, LogOut, BookOpen } from 'lucide-react'

const nav = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload', icon: Upload, label: 'Upload Notes' },
  { to: '/quiz', icon: Brain, label: 'Quiz' },
  { to: '/peers', icon: Users, label: 'Peers' },
]

export default function Layout() {
  const { username, logout } = useAuth()
  const go = useNavigate()

  return (
    <div className="min-h-screen flex bg-gray-50">
      <aside className="w-64 bg-white border-r border-gray-100 flex flex-col fixed h-full">
        <div className="p-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-brand-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-brand-500/20">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold">LearnSync</h1>
              <p className="text-[10px] text-gray-400 uppercase tracking-wider">Smart Learning</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-3 space-y-1">
          {nav.map(({ to, icon: Icon, label }) => (
            <NavLink key={to} to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                  isActive ? 'bg-brand-50 text-brand-700' : 'text-gray-400 hover:bg-gray-50 hover:text-gray-600'
                }`
              }>
              <Icon className="w-[18px] h-[18px]" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 mx-3 mb-3 rounded-xl bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 bg-gradient-to-br from-brand-400 to-indigo-500 rounded-full flex items-center justify-center">
                <span className="text-sm font-bold text-white">{username?.charAt(0)?.toUpperCase()}</span>
              </div>
              <span className="text-sm font-medium text-gray-700">{username}</span>
            </div>
            <button onClick={() => { logout(); go('/login') }}
              className="p-2 text-gray-300 hover:text-red-500 rounded-lg hover:bg-red-50 transition-all">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      <main className="flex-1 ml-64 p-8">
        <Outlet />
      </main>
    </div>
  )
}
