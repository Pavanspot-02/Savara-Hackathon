import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'
import { FileText, Brain, TrendingUp, Upload, ArrowRight, Users } from 'lucide-react'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Dashboard() {
  const { username } = useAuth()
  const [stats, setStats] = useState(null)
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const go = useNavigate()

  useEffect(() => {
    Promise.all([
      api.get('/dashboard').then(r => r.data).catch(() => ({ notes_uploaded: 0, quizzes_taken: 0, avg_score_pct: 0 })),
      api.get('/notes').then(r => r.data).catch(() => []),
    ]).then(([s, n]) => {
      setStats(s)
      setNotes(n.slice(0, 3))
    }).finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner text="Loading dashboard..." />

  const hr = new Date().getHours()
  const greet = hr < 12 ? 'Good morning' : hr < 17 ? 'Good afternoon' : 'Good evening'

  const cards = [
    { l: 'Notes uploaded', v: stats.notes_uploaded, icon: FileText, bg: 'bg-blue-50', ic: 'text-blue-600' },
    { l: 'Quizzes taken', v: stats.quizzes_taken, icon: Brain, bg: 'bg-purple-50', ic: 'text-purple-600' },
    { l: 'Average score', v: `${stats.avg_score_pct}%`, icon: TrendingUp, bg: 'bg-emerald-50', ic: 'text-emerald-600' },
  ]

  return (
    <div className="animate-fade-in max-w-5xl">
      <div className="mb-8">
        <p className="text-sm text-gray-400 mb-1">{greet}</p>
        <h1 className="text-3xl font-bold">{username}</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        {cards.map(({ l, v, icon: Icon, bg, ic }, i) => (
          <div key={l} className="card p-6 animate-slide-up" style={{ animationDelay: `${i * 100}ms` }}>
            <div className={`w-12 h-12 rounded-2xl ${bg} flex items-center justify-center mb-4`}>
              <Icon className={`w-6 h-6 ${ic}`} />
            </div>
            <p className="text-4xl font-bold mb-1">{v}</p>
            <p className="text-sm text-gray-400">{l}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="card p-6">
          <h2 className="text-lg font-semibold mb-4">Quick actions</h2>
          <div className="space-y-3">
            {[
              { i: Upload, l: 'Upload notes', d: 'Get AI summary', to: '/upload', c: 'text-brand-600 bg-brand-50' },
              { i: Brain, l: 'Take a quiz', d: 'Test knowledge', to: '/quiz', c: 'text-purple-600 bg-purple-50' },
              { i: Users, l: 'Find peers', d: 'Study partners', to: '/peers', c: 'text-teal-600 bg-teal-50' },
            ].map(({ i: Icon, l, d, to, c }) => (
              <button key={to} onClick={() => go(to)}
                className="flex items-center justify-between p-4 w-full rounded-xl border border-gray-100 hover:border-brand-200 hover:bg-brand-50/30 transition-all group">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl ${c} flex items-center justify-center`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div className="text-left">
                    <p className="font-medium text-sm">{l}</p>
                    <p className="text-xs text-gray-400">{d}</p>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-gray-300 group-hover:text-brand-600 transition-all" />
              </button>
            ))}
          </div>
        </div>

        <div className="card p-6">
          <h2 className="text-lg font-semibold mb-4">Recent notes</h2>
          {notes.length === 0 ? (
            <div className="py-8 text-center">
              <FileText className="w-10 h-10 text-gray-200 mx-auto mb-3" />
              <p className="text-sm text-gray-400">No notes yet</p>
              <button onClick={() => go('/upload')} className="text-sm text-brand-600 font-medium mt-2 hover:underline">
                Upload first note
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {notes.map((n, i) => (
                <div key={n.id}
                  className="p-3 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer animate-slide-up"
                  style={{ animationDelay: `${(i + 3) * 100}ms` }}
                  onClick={() => go('/quiz', { state: { noteId: n.id } })}>
                  <p className="text-sm font-medium truncate">{n.summary?.slice(0, 60) || n.raw_text?.slice(0, 60)}...</p>
                  <div className="flex gap-1.5 mt-2">
                    {n.concepts?.slice(0, 2).map((c, j) => (
                      <span key={j} className="text-[10px] px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 font-medium">{c.name}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
