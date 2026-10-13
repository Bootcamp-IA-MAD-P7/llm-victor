import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { BriefingForm } from './briefing-form'

const MODELS = [
  { id: 'llama-3.1-8b-instant', label: 'Llama 3.1 8B Instant' },
  { id: 'llama-3.3-70b', label: 'Llama 3.3 70B' },
]

afterEach(() => {
  vi.unstubAllGlobals()
})

function modelsResponse() {
  return new Response(JSON.stringify({ models: MODELS }))
}

function generationResponse(text = 'publicación') {
  return new Response(
    JSON.stringify({ text, provider: 'groq', model: 'llama-3.1-8b-instant' }),
  )
}

function renderForm() {
  const handlers = {
    onResult: vi.fn(),
    onStart: vi.fn(),
    onError: vi.fn(),
  }
  render(<BriefingForm {...handlers} />)
  return handlers
}

function stubFetch(
  generate: () => Promise<Response> = () =>
    Promise.resolve(generationResponse()),
) {
  const fetchMock = vi.fn((input: RequestInfo | URL) => {
    const url = typeof input === 'string' ? input : input.toString()
    if (url.endsWith('/models')) return Promise.resolve(modelsResponse())
    return generate()
  })
  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

function generateCalls(fetchMock: ReturnType<typeof vi.fn>) {
  return fetchMock.mock.calls.filter((call) => {
    const input = call[0] as RequestInfo | URL
    const url = typeof input === 'string' ? input : input.toString()
    return url.endsWith('/generate')
  })
}

async function waitForModels() {
  await waitFor(() =>
    expect(screen.getByLabelText('Modelo')).toHaveValue('llama-3.1-8b-instant'),
  )
}

describe('BriefingForm', () => {
  it('does not call the generation API and warns when the briefing is empty', async () => {
    const fetchMock = stubFetch()
    const handlers = renderForm()
    await waitForModels()

    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Escribe un briefing',
    )
    expect(generateCalls(fetchMock)).toHaveLength(0)
    expect(handlers.onStart).not.toHaveBeenCalled()
  })

  it('rejects a briefing made only of spaces', async () => {
    const fetchMock = stubFetch()
    renderForm()
    await waitForModels()

    await userEvent.type(screen.getByLabelText('Briefing'), '   ')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(generateCalls(fetchMock)).toHaveLength(0)
  })

  it('reports the result for a valid briefing', async () => {
    stubFetch()
    const handlers = renderForm()
    await waitForModels()

    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() =>
      expect(handlers.onResult).toHaveBeenCalledWith({
        text: 'publicación',
        provider: 'groq',
        model: 'llama-3.1-8b-instant',
      }),
    )
  })

  it('disables the button while generating', async () => {
    let resolveGenerate: (value: Response) => void = () => {}
    const pending = new Promise<Response>((resolve) => {
      resolveGenerate = resolve
    })
    stubFetch(() => pending)
    renderForm()
    await waitForModels()

    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(screen.getByRole('button', { name: 'Generar' })).toBeDisabled()

    resolveGenerate(generationResponse('x'))
    await vi.waitFor(() =>
      expect(screen.getByRole('button', { name: 'Generar' })).toBeEnabled(),
    )
  })

  it('reports a comprehensible error and keeps the briefing', async () => {
    stubFetch(() => Promise.reject(new TypeError('Failed to fetch')))
    const handlers = renderForm()
    await waitForModels()

    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() => expect(handlers.onError).toHaveBeenCalled())
    expect(handlers.onError.mock.calls[0][0]).toMatch(/conectar con la API/)
    expect(screen.getByLabelText('Briefing')).toHaveValue('Sobre IA')
  })

  it('offers the audience and tone options and allows changing them', async () => {
    stubFetch()
    renderForm()

    const audience = screen.getByLabelText('Audiencia')
    const tone = screen.getByLabelText('Tono')

    expect(within(audience).getAllByRole('option')).toHaveLength(4)
    expect(within(tone).getAllByRole('option')).toHaveLength(4)

    await userEvent.selectOptions(audience, 'ai-specialists')
    await userEvent.selectOptions(tone, 'inspiring')

    expect(audience).toHaveValue('ai-specialists')
    expect(tone).toHaveValue('inspiring')
  })

  it('offers the four languages with Spanish by default and allows changing them', async () => {
    stubFetch()
    renderForm()

    const language = screen.getByLabelText('Idioma')

    expect(within(language).getAllByRole('option')).toHaveLength(4)
    expect(language).toHaveValue('es')

    await userEvent.selectOptions(language, 'it')

    expect(language).toHaveValue('it')
  })

  it('sends the selected language when generating', async () => {
    const fetchMock = stubFetch()
    renderForm()
    await waitForModels()

    await userEvent.selectOptions(screen.getByLabelText('Idioma'), 'fr')
    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() => expect(generateCalls(fetchMock)).toHaveLength(1))
    const [, init] = generateCalls(fetchMock)[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toMatchObject({
      language: 'fr',
    })
  })

  it('offers the catalog models with the first one selected by default', async () => {
    stubFetch()
    renderForm()

    await waitForModels()

    const model = screen.getByLabelText('Modelo')
    expect(within(model).getAllByRole('option')).toHaveLength(2)
    expect(model).toHaveValue('llama-3.1-8b-instant')
  })

  it('sends the selected model when generating', async () => {
    const fetchMock = stubFetch()
    renderForm()
    await waitForModels()

    await userEvent.selectOptions(
      screen.getByLabelText('Modelo'),
      'llama-3.3-70b',
    )
    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() => expect(generateCalls(fetchMock)).toHaveLength(1))
    const [, init] = generateCalls(fetchMock)[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toMatchObject({
      model: 'llama-3.3-70b',
    })
  })

  it('communicates when the catalog cannot be loaded and disables generation', async () => {
    const fetchMock = vi
      .fn()
      .mockRejectedValue(new TypeError('Failed to fetch'))
    vi.stubGlobal('fetch', fetchMock)
    renderForm()

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'No se pudieron cargar los modelos disponibles',
    )
    expect(screen.getByRole('button', { name: 'Generar' })).toBeDisabled()
  })

  it('refreshes the catalog after the model is no longer available and keeps the briefing', async () => {
    let modelsCalls = 0
    const fetchMock = vi.fn((input: RequestInfo | URL) => {
      const url = typeof input === 'string' ? input : input.toString()
      if (url.endsWith('/models')) {
        modelsCalls += 1
        return Promise.resolve(modelsResponse())
      }
      return Promise.resolve(
        new Response(
          JSON.stringify({ detail: 'Selected model is not available' }),
          {
            status: 409,
          },
        ),
      )
    })
    vi.stubGlobal('fetch', fetchMock)
    const handlers = renderForm()
    await waitForModels()

    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() =>
      expect(handlers.onError).toHaveBeenCalledWith(
        expect.stringMatching(/ya no está disponible/),
      ),
    )
    await vi.waitFor(() => expect(modelsCalls).toBeGreaterThan(1))
    expect(screen.getByLabelText('Briefing')).toHaveValue('Sobre IA')
  })
})
