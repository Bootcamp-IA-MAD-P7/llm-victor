import { useEffect, useState } from 'react'

import { Button } from '@/components/ui/button'
import { checkApiHealth } from '@/lib/api'
import { cn } from '@/lib/utils'

type Status = 'checking' | 'available' | 'unavailable'

const LABELS: Record<Status, string> = {
  checking: 'Comprobando la API…',
  available: 'API disponible',
  unavailable: 'La API no está disponible',
}

const DOT_COLORS: Record<Status, string> = {
  checking: 'bg-muted-foreground',
  available: 'bg-emerald-500',
  unavailable: 'bg-destructive',
}

export function ApiStatus() {
  const [status, setStatus] = useState<Status>('checking')
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let active = true
    void checkApiHealth().then((ok) => {
      if (active) setStatus(ok ? 'available' : 'unavailable')
    })
    return () => {
      active = false
    }
  }, [attempt])

  function retry() {
    setStatus('checking')
    setAttempt((n) => n + 1)
  }

  return (
    <div className="flex items-center gap-3">
      <p role="status" className="flex items-center gap-2 text-sm">
        <span className={cn('size-2 rounded-full', DOT_COLORS[status])} />
        {LABELS[status]}
      </p>
      {status === 'unavailable' && (
        <Button variant="outline" size="sm" onClick={retry}>
          Reintentar
        </Button>
      )}
    </div>
  )
}
