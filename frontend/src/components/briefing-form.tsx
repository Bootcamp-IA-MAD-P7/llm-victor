import { useState } from 'react'

import { Button } from '@/components/ui/button'
import { generatePost } from '@/lib/api'

interface Props {
  onResult: (text: string) => void
  onStart: () => void
  onError: () => void
}

export function BriefingForm({ onResult, onStart, onError }: Props) {
  const [brief, setBrief] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!brief.trim()) return
    onStart()
    try {
      const res = await generatePost({ brief })
      onResult(res.text)
    } catch (err) {
      console.error(err)
      onError()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <label className="block text-sm font-medium">
        Briefing
        <textarea
          className="mt-1 w-full rounded-md border p-2"
          rows={6}
          value={brief}
          onChange={(e) => setBrief(e.target.value)}
          placeholder="Escribe el briefing para generar una publicación de LinkedIn..."
          required
        />
      </label>
      <Button type="submit">Generar</Button>
    </form>
  )
}
