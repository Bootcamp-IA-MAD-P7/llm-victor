interface Props {
  text: string
  provider: string
  model: string
}

export function ResultView({ text, provider, model }: Props) {
  return (
    <div className="space-y-2">
      <h2 className="text-lg font-medium">Resultado</h2>
      <pre className="whitespace-pre-wrap rounded-md border bg-muted p-4 text-sm">
        {text}
      </pre>
      <p className="text-xs text-muted-foreground">
        Generado con {provider} · {model}
      </p>
      <p className="text-xs text-muted-foreground">
        Listo para revisar. No se publica automáticamente.
      </p>
    </div>
  )
}
