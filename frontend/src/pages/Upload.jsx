import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import { Sparkles, ArrowRight, FileText, Zap, Copy, Check, ImagePlus, X, Camera } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Upload() {
  const [mode, setMode] = useState('text')
  const [text, setText] = useState('')
  const [img, setImg] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [copied, setCopied] = useState(false)
  const [drag, setDrag] = useState(false)
  const ref = useRef(null)
  const go = useNavigate()

  const pickImg = (f) => {
    if (!f) return
    if (f.size > 10485760) return toast.error('Max 10MB')
    setImg(f)
    const reader = new FileReader()
    reader.onload = (e) => setPreview(e.target.result)
    reader.readAsDataURL(f)
  }

  const uploadText = async () => {
    if (text.trim().length < 20) return toast.error('Min 20 characters')
    setLoading(true); setResult(null)
    try {
      const r = await api.post('/notes', { raw_text: text })
      setResult(r.data)
      toast.success('Analyzed!')
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Failed')
    } finally { setLoading(false) }
  }

  const uploadImg = async () => {
    if (!img) return
    setLoading(true); setResult(null)
    try {
      const fd = new FormData()
      fd.append('file', img)
      const r = await api.post('/notes/image', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000,
      })
      setResult(r.data)
      toast.success('Scanned & analyzed!')
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Failed')
    } finally { setLoading(false) }
  }

  const copy = () => {
    navigator.clipboard.writeText(result.summary)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const clear = () => {
    setImg(null); setPreview(null)
    if (ref.current) ref.current.value = ''
  }

  const cc = text.length
  const ccl = cc < 20 ? 'text-red-400' : cc < 100 ? 'text-amber-400' : 'text-emerald-400'

  return (
    <div className="animate-fade-in max-w-4xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Upload Notes</h1>
        <p className="text-gray-400 mt-1 text-sm">Paste text or scan handwritten notes with AI</p>
      </div>

      {/* Mode toggle */}
      <div className="flex gap-2 mb-6 p-1 bg-gray-100 rounded-xl w-fit">
        <button onClick={() => setMode('text')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${mode === 'text' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500'}`}>
          <FileText className="w-4 h-4" /> Paste Text
        </button>
        <button onClick={() => setMode('image')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${mode === 'image' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500'}`}>
          <Camera className="w-4 h-4" /> Scan Handwritten
        </button>
      </div>

      {/* Text mode */}
      {mode === 'text' && (
        <div className="card p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-brand-50 rounded-lg flex items-center justify-center">
                <FileText className="w-4 h-4 text-brand-600" />
              </div>
              <h2 className="font-semibold text-sm">Lecture notes</h2>
            </div>
            <span className={`text-xs font-mono font-medium ${ccl}`}>{cc} chars</span>
          </div>
          <textarea value={text} onChange={(e) => setText(e.target.value)}
            placeholder="Paste your lecture notes here..."
            className="input-field min-h-[220px] resize-y font-mono text-sm leading-relaxed"
            disabled={loading} />
          <div className="flex justify-end mt-4">
            <button onClick={uploadText} disabled={loading || text.trim().length < 20}
              className="btn-primary flex items-center gap-2 px-6">
              {loading
                ? <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Analyzing...</>
                : <><Zap className="w-4 h-4" />Analyze</>
              }
            </button>
          </div>
        </div>
      )}

      {/* Image mode */}
      {mode === 'image' && (
        <div className="card p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 bg-purple-50 rounded-lg flex items-center justify-center">
              <Camera className="w-4 h-4 text-purple-600" />
            </div>
            <h2 className="font-semibold text-sm">Scan handwritten notes</h2>
          </div>

          {!preview ? (
            <div
              onDragOver={(e) => { e.preventDefault(); setDrag(true) }}
              onDragLeave={() => setDrag(false)}
              onDrop={(e) => { e.preventDefault(); setDrag(false); pickImg(e.dataTransfer.files[0]) }}
              onClick={() => ref.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${
                drag ? 'border-brand-400 bg-brand-50/50' : 'border-gray-200 hover:border-brand-300'
              }`}>
              <ImagePlus className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600 font-medium mb-1">Drop handwritten notes here</p>
              <p className="text-sm text-gray-400">PNG, JPG, WEBP up to 10MB</p>
            </div>
          ) : (
            <div className="relative">
              <img src={preview} alt="Note" className="w-full max-h-[400px] object-contain rounded-xl border border-gray-100" />
              <button onClick={clear}
                className="absolute top-3 right-3 w-8 h-8 bg-white/90 rounded-full flex items-center justify-center shadow-md hover:bg-red-50">
                <X className="w-4 h-4" />
              </button>
              <p className="text-xs text-gray-400 mt-2">{img?.name} ({(img?.size / 1024).toFixed(0)} KB)</p>
            </div>
          )}

          <input ref={ref} type="file" accept="image/*" onChange={(e) => pickImg(e.target.files[0])} className="hidden" />

          {preview && (
            <div className="flex justify-end mt-4">
              <button onClick={uploadImg} disabled={loading}
                className="btn-primary flex items-center gap-2 px-6">
                {loading
                  ? <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Scanning...</>
                  : <><Sparkles className="w-4 h-4" />Scan & Analyze</>
                }
              </button>
            </div>
          )}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="card p-10 text-center animate-fade-in">
          <div className="relative w-16 h-16 mx-auto mb-5">
            <div className="absolute inset-0 border-[3px] border-brand-100 rounded-full" />
            <div className="absolute inset-0 border-[3px] border-brand-600 border-t-transparent rounded-full animate-spin" />
            <Sparkles className="w-6 h-6 text-brand-600 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
          </div>
          <p className="font-semibold">{mode === 'image' ? 'Reading handwriting...' : 'Analyzing notes...'}</p>
          <p className="text-sm text-gray-400 mt-1">This may take a moment</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-5 animate-slide-up">
          <div className="card p-6 border-l-4 border-l-brand-500">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-amber-500" />
                <h2 className="font-semibold">AI Summary</h2>
                {mode === 'image' && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-50 text-purple-600 font-medium">handwritten scan</span>
                )}
              </div>
              <button onClick={copy} className="btn-ghost text-xs flex items-center gap-1.5 py-1.5 px-3">
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
            <p className="text-gray-600 leading-relaxed">{result.summary}</p>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold">Key Concepts</h2>
              <span className="text-xs text-gray-400">{result.concepts.length} extracted</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {result.concepts.map((c, i) => (
                <span key={i} className="concept-tag animate-slide-up" style={{ animationDelay: `${i * 60}ms` }}>
                  {c.name}
                  <span className="ml-1.5 opacity-50 text-[10px]">{Math.round(c.score * 100)}%</span>
                </span>
              ))}
            </div>
          </div>

          <div className="flex gap-3">
            <button onClick={() => go('/quiz', { state: { noteId: result.note_id } })}
              className="btn-primary flex items-center gap-2">
              Take Quiz <ArrowRight className="w-4 h-4" />
            </button>
            <button onClick={() => { setResult(null); setText(''); clear() }} className="btn-secondary">
              Upload Another
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
