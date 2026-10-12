import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { BriefingForm } from './briefing-form'

afterEach(() => {
  vi.unstubAllGlobals()
})

function renderForm() {
  const handlers = {
    onResult: vi.fn(),
    onStart: vi.fn(),
    onError: vi.fn(),
  }
  render(<BriefingForm {...handlers} />)
  return handlers
}

describe('BriefingForm', () => {
  it('does not call the API and warns when the briefing is empty', async () => {
    const fetchMock = vi.fn()
    vi.stubGlobal('fetch', fetchMock)
    const handlers = renderForm()

    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Escribe un briefing',
    )
    expect(fetchMock).not.toHaveBeenCalled()
    expect(handlers.onStart).not.toHaveBeenCalled()
  })

  it('rejects a briefing made only of spaces', async () => {
    const fetchMock = vi.fn()
    vi.stubGlobal('fetch', fetchMock)
    renderForm()

    await userEvent.type(screen.getByLabelText('Briefing'), '   ')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('reports the result for a valid briefing', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            text: 'publicación',
            provider: 'groq',
            model: 'x',
          }),
        ),
      ),
    )
    const handlers = renderForm()

    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() =>
      expect(handlers.onResult).toHaveBeenCalledWith('publicación'),
    )
  })

  it('disables the button while generating', async () => {
    let resolveFetch: (value: Response) => void = () => {}
    const pending = new Promise<Response>((resolve) => {
      resolveFetch = resolve
    })
    vi.stubGlobal('fetch', vi.fn().mockReturnValue(pending))
    renderForm()

    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    expect(screen.getByRole('button', { name: 'Generar' })).toBeDisabled()

    resolveFetch(
      new Response(JSON.stringify({ text: 'x', provider: 'groq', model: 'x' })),
    )
    await vi.waitFor(() =>
      expect(screen.getByRole('button', { name: 'Generar' })).toBeEnabled(),
    )
  })

  it('reports a comprehensible error and keeps the briefing', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockRejectedValue(new TypeError('Failed to fetch')),
    )
    const handlers = renderForm()

    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() => expect(handlers.onError).toHaveBeenCalled())
    expect(handlers.onError.mock.calls[0][0]).toMatch(/conectar con la API/)
    expect(screen.getByLabelText('Briefing')).toHaveValue('Sobre IA')
  })

  it('offers the audience and tone options and allows changing them', async () => {
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

  it('sends the selected audience and tone when generating', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(
        new Response(
          JSON.stringify({ text: 'publicación', provider: 'groq', model: 'x' }),
        ),
      )
    vi.stubGlobal('fetch', fetchMock)
    renderForm()

    await userEvent.selectOptions(
      screen.getByLabelText('Audiencia'),
      'business-leaders',
    )
    await userEvent.selectOptions(screen.getByLabelText('Tono'), 'educational')
    await userEvent.type(screen.getByLabelText('Briefing'), 'Sobre IA')
    await userEvent.click(screen.getByRole('button', { name: 'Generar' }))

    await vi.waitFor(() => expect(fetchMock).toHaveBeenCalled())
    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(JSON.parse(init.body as string)).toEqual({
      brief: 'Sobre IA',
      audience: 'business-leaders',
      tone: 'educational',
    })
  })
})
