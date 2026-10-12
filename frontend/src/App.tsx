import { ApiStatus } from '@/components/api-status'

function App() {
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
    </main>
  )
}

export default App
