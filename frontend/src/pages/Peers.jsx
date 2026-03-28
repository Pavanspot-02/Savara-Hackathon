import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import { Users, UserPlus, Upload } from 'lucide-react'
import LoadingSpinner from '../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function Peers() {
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const go = useNavigate()

  useEffect(() => {
    api.get('/peers')
      .then(r => setMatches(r.data.matches))
      .catch(() => toast.error('Failed to load peers'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner text="Finding study partners..." />

  return (
    <div className="animate-fade-in max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Peer Matches</h1>
        <p className="text-gray-400 mt-1 text-sm">Students who share similar learning topics</p>
      </div>

      {matches.length === 0 ? (
        <div className="card p-12 text-center">
          <Users className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 font-medium">No matches yet</p>
          <p className="text-sm text-gray-400 mt-1 mb-4">Upload more notes to find peers</p>
          <button onClick={() => go('/upload')}
            className="btn-primary flex items-center gap-2 mx-auto">
            <Upload className="w-4 h-4" /> Upload Notes
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {matches.map((m, i) => (
            <div key={m.user_id} className="card p-6 animate-slide-up" style={{ animationDelay: `${i * 80}ms` }}>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-brand-100 rounded-full flex items-center justify-center">
                    <span className="text-lg font-bold text-brand-700">{m.username.charAt(0).toUpperCase()}</span>
                  </div>
                  <div>
                    <h3 className="font-semibold">{m.username}</h3>
                    <p className="text-sm text-gray-400">{Math.round(m.match_score * 100)}% topic overlap</p>
                  </div>
                </div>
                <button className="btn-secondary text-sm flex items-center gap-1.5 py-2 px-4">
                  <UserPlus className="w-3.5 h-3.5" /> Connect
                </button>
              </div>
              <div className="mt-4 pt-4 border-t border-gray-50">
                <p className="text-xs text-gray-400 mb-2">Shared topics</p>
                <div className="flex flex-wrap gap-2">
                  {m.shared_concepts.map((c, j) => (
                    <span key={j} className="concept-tag text-[10px]">{c}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
