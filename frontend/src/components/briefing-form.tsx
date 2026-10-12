import { useState } from 'react'

import { Button } from '@/components/ui/button'
import type { Audience, Tone } from '@/lib/api'
import { generatePost, generationErrorMessage } from '@/lib/api'
import {
  AUDIENCE_OPTIONS,
  DEFAULT_AUDIENCE,
  DEFAULT_TONE,
  TONE_OPTIONS,
} from '@/lib/generation-options'

interface Props {
  onResult: (text: string) => void
  onStart: () => void
  onError: (message: string) => void
}

export function BriefingForm({ onResult, onStart, onError }: Props) {
  const [brief, setBrief] = useState('')
  const [audience, setAudience] = useState<Audience>(DEFAULT_AUDIENCE)
  const [tone, setTone] = useState<Tone>(DEFAULT_TONE)
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
      const res = await generatePost({ brief: trimmed, audience, tone })
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
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="block text-sm font-medium">
          Audiencia
          <select
            className="mt-1 w-full rounded-md border p-2"
            value={audience}
            onChange={(e) => setAudience(e.target.value as Audience)}
          >
            {AUDIENCE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
        <label className="block text-sm font-medium">
          Tono
          <select
            className="mt-1 w-full rounded-md border p-2"
            value={tone}
            onChange={(e) => setTone(e.target.value as Tone)}
          >
            {TONE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
      </div>
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
