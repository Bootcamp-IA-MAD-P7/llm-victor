import { useState } from 'react'

import { Button } from '@/components/ui/button'
import { generatePost, generationErrorMessage } from '@/lib/api'

interface Props {
  onResult: (text: string) => void
  onStart: () => void
  onError: (message: string) => void
}

export function BriefingForm({ onResult, onStart, onError }: Props) {
  const [brief, setBrief] = useState('')
  const [validationError, setValidationError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (submitting) return

    const trimmed = brief.trim()
    if (!trimmed) {
      setValidationError('Escribe un briefing para generar la publicación.')
      return
    }

    setValidationError('')
    setSubmitting(true)
    onStart()
    try {
      const res = await generatePost({ brief: trimmed })
      onResult(res.text)
    } catch (err) {
      onError(generationErrorMessage(err))
    } finally {
      setSubmitting(false)
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
          onChange={(e) => {
            setBrief(e.target.value)
            if (validationError) setValidationError('')
          }}
          aria-invalid={validationError ? true : undefined}
          placeholder="Escribe el briefing para generar una publicación de LinkedIn..."
        />
      </label>
      {validationError && (
        <p role="alert" className="text-sm text-destructive">
          {validationError}
        </p>
      )}
      <Button type="submit" disabled={submitting}>
        Generar
      </Button>
    </form>
  )
}
