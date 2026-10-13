import { useState } from 'react'

import { ApiStatus } from '@/components/api-status'
import { BriefingForm } from '@/components/briefing-form'
import { ResultView } from '@/components/result-view'
import type { GenerateResponse } from '@/lib/api'

type State = 'idle' | 'loading' | 'done' | 'error'

function App() {
  const [state, setState] = useState<State>('idle')
  const [result, setResult] = useState<GenerateResponse | null>(null)
  const [error, setError] = useState('')

  return (
    <main className="mx-auto flex min-h-svh max-w-2xl flex-col justify-center gap-6 px-4">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">
          AI Content Studio
        </h1>
        <p className="text-muted-foreground">
          Del briefing a una publicación de LinkedIn sobre inteligencia
          artificial.
        </p>
      </div>
      <ApiStatus />
      <BriefingForm
        onStart={() => {
          setError('')
          setState('loading')
        }}
        onResult={(generated) => {
          setResult(generated)
          setState('done')
        }}
        onError={(message) => {
          setError(message)
          setState('error')
        }}
      />
      {state === 'loading' && <p role="status">Generando…</p>}
      {state === 'error' && (
        <p role="alert" className="text-destructive">
          {error}
        </p>
      )}
      {state === 'done' && result && (
        <ResultView
          text={result.text}
          provider={result.provider}
          model={result.model}
        />
      )}
    </main>
  )
}

export default App
