import { Sparkles } from 'lucide-react'

export default function LoadingSpinner({ text = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 animate-fade-in">
      <div className="relative w-12 h-12 mb-5">
        <div className="absolute inset-0 border-[3px] border-brand-100 rounded-full" />
        <div className="absolute inset-0 border-[3px] border-brand-600 border-t-transparent rounded-full animate-spin" />
        <Sparkles className="w-5 h-5 text-brand-500 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
      </div>
      <p className="text-sm text-gray-400 font-medium">{text}</p>
    </div>
  )
}
