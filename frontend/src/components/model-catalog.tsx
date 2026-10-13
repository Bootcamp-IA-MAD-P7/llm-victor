import { useEffect, useState } from 'react'

import type { Model } from '@/lib/api'
import { fetchModels } from '@/lib/api'

export function ModelCatalog() {
  const [models, setModels] = useState<Model[]>([])
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let active = true
    fetchModels()
      .then((result) => {
        if (active) setModels(result)
      })
      .catch(() => {
        if (active) setFailed(true)
      })
    return () => {
      active = false
    }
  }, [])

  return (
    <section className="space-y-2">
      <h2 className="text-sm font-medium">Modelos disponibles</h2>
      {failed ? (
        <p role="alert" className="text-sm text-destructive">
          No se pudieron cargar los modelos disponibles.
        </p>
      ) : (
        <ul className="list-disc pl-5 text-sm text-muted-foreground">
          {models.map((model) => (
            <li key={model.id}>{model.label}</li>
          ))}
        </ul>
      )}
    </section>
  )
}
