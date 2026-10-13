import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import App from './App'

afterEach(() => {
  vi.unstubAllGlobals()
})

function stubFetch(
  generate: () => Promise<Response>,
  health: () => Promise<Response> = () =>
    Promise.resolve(new Response('{"status":"ok"}')),
  models: () => Promise<Response> = () =>
    Promise.resolve(new Response('{"models":[]}')),
) {
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo | URL) => {
      const url = typeof input === 'string' ? input : input.toString()
      if (url.endsWith('/health')) return health()
      if (url.endsWith('/models')) return models()
      return generate()
    }),
  )
}

describe('App', () => {
  it('shows a loading state while generating and then the result', async () => {
    let resolveGenerate: (value: Response) => void = () => {}
    const pending = new Promise<Response>((resolve) => {
      resolveGenerate = resolve
    })
    stubFetch(() => pending)

    render(<App />)
    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(screen.getByText('Generando…')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Generar' })).toBeDisabled()

    resolveGenerate(
      new Response(
        JSON.stringify({ text: 'resultado', provider: 'groq', model: 'x' }),
      ),
    )
    expect(await screen.findByText('resultado')).toBeInTheDocument()
  })

  it('shows a comprehensible error and keeps the briefing to retry', async () => {
    stubFetch(() => Promise.reject(new TypeError('Failed to fetch')))

    render(<App />)
    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      /conectar con la API/,
    )
    expect(screen.getByLabelText('Briefing')).toHaveValue('Sobre IA')
    expect(screen.getByRole('button', { name: 'Generar' })).toBeEnabled()
  })
})
