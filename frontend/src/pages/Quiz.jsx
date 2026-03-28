import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import api from '../api/client'
import { Brain, CheckCircle, XCircle, ArrowRight, Trophy, RotateCcw } from 'lucide-react'
import LoadingSpinner from '../components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function Quiz() {
  const loc = useLocation()
  const go = useNavigate()
  const noteId = loc.state?.noteId

  const [notes, setNotes] = useState([])
  const [selId, setSelId] = useState(noteId || null)
  const [qs, setQs] = useState([])
  const [cur, setCur] = useState(0)
  const [sel, setSel] = useState(null)
  const [sub, setSub] = useState(false)
  const [score, setScore] = useState(0)
  const [ans, setAns] = useState([])
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(false)
  const [ln, setLn] = useState(true)

  useEffect(() => {
    api.get('/notes')
      .then(r => {
        setNotes(r.data.filter(n => n.summary))
        if (noteId) loadQ(noteId)
      })
      .catch(() => {})
      .finally(() => setLn(false))
  }, [])

  const loadQ = async (id) => {
    setLoading(true); setDone(false); setCur(0); setScore(0); setAns([]); setSel(null); setSub(false)
    try {
      const r = await api.get(`/quiz/${id}`)
      setQs(r.data.questions)
      setSelId(id)
    } catch (e) {
      toast.error('Failed to generate quiz')
    } finally { setLoading(false) }
  }

  const check = () => {
    if (!sel) return
    const ok = sel === qs[cur].correct
    if (ok) setScore(s => s + 1)
    setAns(a => [...a, { question_id: qs[cur].id, selected: sel, correct: ok }])
    setSub(true)
  }

  const next = () => {
    if (cur + 1 >= qs.length) {
      setDone(true)
      api.post('/quiz/submit', { note_id: selId, score, total: qs.length, answers: ans }).catch(() => {})
      return
    }
    setCur(c => c + 1); setSel(null); setSub(false)
  }

  // Note selection
  if (!selId || qs.length === 0) {
    if (ln) return <LoadingSpinner text="Loading notes..." />
    if (loading) return <LoadingSpinner text="Generating quiz..." />

    return (
      <div className="animate-fade-in max-w-2xl">
        <div className="mb-8">
          <h1 className="text-2xl font-bold">Quiz</h1>
          <p className="text-gray-400 mt-1 text-sm">Select a note to quiz yourself</p>
        </div>
        {notes.length === 0 ? (
          <div className="card p-12 text-center">
            <Brain className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 font-medium">No notes yet</p>
            <button onClick={() => go('/upload')} className="btn-primary mt-4">Upload Notes</button>
          </div>
        ) : (
          <div className="space-y-3">
            {notes.map(n => (
              <button key={n.id} onClick={() => loadQ(n.id)}
                className="card p-5 w-full text-left hover:border-brand-200 transition-all group">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium truncate">{n.summary?.slice(0, 80)}...</p>
                    <div className="flex gap-2 mt-2">
                      {n.concepts?.slice(0, 3).map((c, i) => (
                        <span key={i} className="concept-tag text-[10px]">{c.name}</span>
                      ))}
                    </div>
                  </div>
                  <ArrowRight className="w-5 h-5 text-gray-300 group-hover:text-brand-600 ml-4" />
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    )
  }

  // Finished
  if (done) {
    const pct = Math.round(score / qs.length * 100)
    return (
      <div className="animate-fade-in max-w-lg mx-auto text-center py-12">
        <div className="card p-10">
          <Trophy className={`w-16 h-16 mx-auto mb-6 ${pct >= 60 ? 'text-amber-400' : 'text-gray-300'}`} />
          <h2 className="text-3xl font-bold mb-2">{score}/{qs.length}</h2>
          <p className="text-gray-400 mb-6">{pct >= 80 ? 'Excellent!' : pct >= 60 ? 'Good job!' : 'Keep practicing!'}</p>
          <div className="w-full bg-gray-100 rounded-full h-3 mb-8">
            <div className={`h-3 rounded-full transition-all duration-1000 ${pct >= 80 ? 'bg-emerald-500' : pct >= 60 ? 'bg-amber-500' : 'bg-red-400'}`}
              style={{ width: `${pct}%` }} />
          </div>
          <div className="flex gap-3 justify-center">
            <button onClick={() => loadQ(selId)} className="btn-secondary flex items-center gap-2">
              <RotateCcw className="w-4 h-4" /> Retry
            </button>
            <button onClick={() => { setSelId(null); setQs([]) }} className="btn-primary">New Quiz</button>
          </div>
        </div>
      </div>
    )
  }

  // Quiz question
  const q = qs[cur]

  return (
    <div className="animate-fade-in max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <span className="text-sm text-gray-400">Question {cur + 1} of {qs.length}</span>
        <span className="text-sm font-medium text-brand-600">Score: {score}</span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-1.5 mb-8">
        <div className="bg-brand-600 h-1.5 rounded-full transition-all duration-500"
          style={{ width: `${(cur + 1) / qs.length * 100}%` }} />
      </div>

      <div className="card p-8 mb-6">
        <h2 className="text-lg font-semibold leading-relaxed">{q.question}</h2>
      </div>

      <div className="space-y-3 mb-8">
        {q.options.map(o => {
          let cl = 'card p-4 w-full text-left cursor-pointer transition-all duration-200'
          if (sub) {
            if (o.label === q.correct) cl += ' border-emerald-300 bg-emerald-50'
            else if (o.label === sel && o.label !== q.correct) cl += ' border-red-300 bg-red-50'
            else cl += ' opacity-50'
          } else if (sel === o.label) {
            cl += ' border-brand-300 bg-brand-50 ring-2 ring-brand-500/20'
          }

          return (
            <button key={o.label} onClick={() => !sub && setSel(o.label)} className={cl} disabled={sub}>
              <div className="flex items-center gap-4">
                <span className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold ${
                  sel === o.label ? 'bg-brand-600 text-white' : 'bg-gray-100 text-gray-500'
                }`}>{o.label}</span>
                <span className="text-sm">{o.text}</span>
                {sub && o.label === q.correct && <CheckCircle className="w-5 h-5 text-emerald-500 ml-auto" />}
                {sub && o.label === sel && o.label !== q.correct && <XCircle className="w-5 h-5 text-red-400 ml-auto" />}
              </div>
            </button>
          )
        })}
      </div>

      {!sub ? (
        <button onClick={check} disabled={!sel} className="btn-primary w-full">Check Answer</button>
      ) : (
        <button onClick={next} className="btn-primary w-full flex items-center justify-center gap-2">
          {cur + 1 >= qs.length ? 'See Results' : 'Next Question'} <ArrowRight className="w-4 h-4" />
        </button>
      )}
    </div>
  )
}
